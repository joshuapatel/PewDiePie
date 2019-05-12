# -> Discord
import discord
from discord.ext import commands
from discord.ext import tasks
# -> Loop
import aiohttp
import asyncio
# -> Miscellaneous
import datetime
# -> Configuration
import sys
sys.path.append("../")
import config


class Subscribe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.subgap_task.start()

    def cog_unload(self):
        self.subgap_task.cancel()

    @tasks.loop(seconds = 15)
    async def subgap_task(self):
        guilds = await self.bot.pool.fetch("SELECT * FROM subgap")

        for msg, ch, gd in guilds:
            await self.subgcheck(gd, ch, msg)

    @subgap_task.before_loop
    async def before_subgap_task(self):
        await self.bot.wait_until_ready()

    async def subgcheck(self, guild, channel, message):
        check = self.bot.get_channel(channel)

        if not check:
            await self.bot.pool.execute("DELETE FROM subgap WHERE guildid = $1", guild)
            return

        try:
            msg = await check.fetch_message(message)
        except (discord.NotFound, discord.Forbidden):
            await self.bot.pool.execute("DELETE FROM subgap WHERE guildid = $1", guild)
            return

        ctx = await self.bot.get_context(msg)
        sub_msg = await ctx.invoke(self.bot.get_command("subcount"), _type = "False")
        await self.subgedit(channel, message, msg = sub_msg)

    async def subgedit(self, channel, message, msg = None, embed = None):
        if msg:
            em = discord.Embed(color = discord.Color.blurple())
            em.add_field(name = "Leading Channel", value = msg)
            em.timestamp = datetime.datetime.utcnow()
        else:
            em = None

        channel = self.bot.get_channel(channel)
        message = await channel.fetch_message(message)
        await message.edit(embed = em or embed)

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def setup(self, ctx):
        base_uri = "https://www.googleapis.com/youtube/v3/search"

        def check(message):
            if message.channel.id != ctx.channel.id:
                return False
            if message.author.id != ctx.author.id:
                return False

            return True

        async def search(ch_name):
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{base_uri}?part=snippet&maxResults=1&q={ch_name}&type=channel&key={config.ytdapi}") as ch:
                    channel = await ch.json()

            return channel

        await ctx.send("Please enter the first YouTuber's channel name.")
        try:
            first_ch = await self.bot.wait_for("message", check = check, timeout = 30)
        except asyncio.TimeoutError:
            return

        first_search = await search(first_ch.content)

        if first_search["pageInfo"]["totalResults"] >= 1:
            first_ch = first_search["items"][0]["id"]["channelId"]
        else:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "YouTuber Not Found", value = "Couldn't find a YouTuber with that name.")
            await ctx.send(embed = em)
            return

        await ctx.send("Please enter the second YouTuber's channel name.")
        try:
            second_ch = await self.bot.wait_for("message", check = check, timeout = 30)
        except asyncio.TimeoutError:
            return

        second_search = await search(second_ch.content)

        if second_search["pageInfo"]["totalResults"] >= 1:
            second_ch = second_search["items"][0]["id"]["channelId"]
        else:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "YouTuber Not Found", value = "Couldn't find a YouTuber with that name.")
            await ctx.send(embed = em)
            return

        guild_check = await self.bot.pool.fetchrow("SELECT * FROM sub_setup WHERE guildid = $1", ctx.guild.id)
        if guild_check is None:
            await self.bot.pool.execute("INSERT INTO sub_setup VALUES ($1, $2, $3)", ctx.guild.id, first_ch, second_ch)
        else:
            await self.bot.pool.execute("UPDATE sub_setup SET first_ch = $1, second_ch = $2 WHERE guildid = $3",
                first_ch, second_ch, ctx.guild.id)

        await ctx.send("Completed setup!")

    @commands.group(invoke_without_command = True)
    @commands.has_permissions(manage_guild = True)
    async def subgap(self, ctx):
        chtwo = await self.bot.pool.fetchrow("SELECT * FROM subgap WHERE guildid = $1", ctx.guild.id)
        if chtwo is not None:
            prefix = ctx.prefix.replace(self.bot.user.mention, f"@{self.bot.user.name}")
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Subscriber Gap in Use",
            value = f"The subgap command is being used in your server already. Please delete the subgap message and wait 30 seconds or run `{prefix}subgap stop`.")
            await ctx.send(embed = em)
            return

        info = await ctx.invoke(self.bot.get_command("subcount"), _type = "False")
        em = discord.Embed(color = discord.Color.blurple())
        em.add_field(name = "Leading Channel", value = info)
        em.timestamp = datetime.datetime.utcnow()
        stmsg = await ctx.send(embed = em)

        await self.bot.pool.execute("INSERT INTO subgap VALUES ($1, $2, $3)", stmsg.id, ctx.channel.id, ctx.guild.id)

    @subgap.command(aliases = ["remove", "delete"])
    @commands.has_permissions(manage_guild = True)
    async def stop(self, ctx):
        c = await self.bot.pool.fetchrow("SELECT * FROM subgap WHERE guildid = $1", ctx.guild.id)

        if c is None:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Subscriber Gap Not Running", value = "The subgap command is not currently being used in your server.")
            await ctx.send(embed = em)
            return

        await self.bot.pool.execute("DELETE FROM subgap WHERE guildid = $1", ctx.guild.id)

        em = discord.Embed(color = discord.Color.dark_red())
        em.add_field(name = "Subscriber Gap Stopped", value = "The subgap message has stopped updating in your server.")
        await ctx.send(embed = em)

    @commands.command(aliases = ["subscribercount", "sc"])
    async def subcount(self, ctx, _type: str = "True"):
        _type = _type != "False"

        if _type: await ctx.channel.trigger_typing()

        base_uri = "https://www.googleapis.com/youtube/v3/channels"

        youtuber = await self.bot.pool.fetchrow("SELECT first_ch, second_ch FROM sub_setup WHERE guildid = $1", ctx.guild.id)
        if youtuber is None:
            first_ch = "UC-lHJZR3Gqxm24_Vd_AJ5Yw"
            second_ch = "UCq-Fj5jknLsUf-MWSy4_brA"
        else:
            first_ch, second_ch = youtuber

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_uri}?part=snippet,contentDetails,statistics&id={first_ch}&key={config.ytdapi}") as fh:
                first_ch = await fh.json()
            async with session.get(f"{base_uri}?part=snippet,contentDetails,statistics&id={second_ch}&key={config.ytdapi}") as sh:
                second_ch = await sh.json()

        first_count = int(first_ch["items"][0]["statistics"]["subscriberCount"])
        second_count = int(second_ch["items"][0]["statistics"]["subscriberCount"])

        first_name = first_ch["items"][0]["snippet"]["title"]
        second_name = second_ch["items"][0]["snippet"]["title"]

        if first_count >= second_count:
            sg = f"{first_name} is leading with {first_count - second_count:,d} more subscribers than {second_name}"
        else:
            sg = f"{second_name} is leading with {second_count - first_count:,d} more subscribers than {first_name}"

        if not _type: return sg

        em = discord.Embed(color = discord.Color.red())
        em.add_field(name = first_name, value = f"{first_count:,d}")
        em.add_field(name = second_name, value = f"{second_count:,d}")
        em.add_field(name = "Leading Channel", value = sg, inline = False)
        await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Subscribe(bot))
