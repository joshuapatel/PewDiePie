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


async def get_message(bot, channel, msgid):
    """Checks for a message by its ID in the internal cache. Resorts to an API call if not found"""
    t = discord.utils.get(bot.cached_messages, id = msgid)
    if t is not None:
        return t
    else:
        return await channel.fetch_message(msgid)

class Subscribe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sg = {}
        self.subgap_task.start() # pylint: disable=no-member

    def cog_unload(self):
        self.subgap_task.cancel() # pylint: disable=no-member

    @tasks.loop(seconds = 15)
    async def subgap_task(self):
        guilds = await self.bot.pool.fetch("SELECT * FROM subgap")
        self.sg.clear()

        for msg, ch, gd in guilds:
            await self.subgap_check(gd, ch, msg)

    @subgap_task.before_loop
    async def before_subgap_task(self):
        await self.bot.wait_until_ready()

    async def subgap_check(self, guild, channel, message):
        check = self.bot.get_channel(channel)

        if not check:
            await self.bot.pool.execute("DELETE FROM subgap WHERE guildid = $1", guild)
            return

        try:
            await get_message(self.bot, check, message)
        except (discord.NotFound, discord.Forbidden):
            await self.bot.pool.execute("DELETE FROM subgap WHERE guildid = $1", guild)
            return

        guild_sub = await self.get_guild_sub(guild)

        if guild_sub[0] in self.sg:
            sub_msg = self.sg[guild_sub[0]][2]
        else:
            info = await self.get_channel_info(*guild_sub)
            self.sg[guild_sub[0]] = info[0]
            sub_msg = info[0][2]

        if guild_sub[1] in self.sg:
            sub_msg = self.sg[guild_sub[1]][2]
        else:
            info = await self.get_channel_info(*guild_sub)
            self.sg[guild_sub[1]] = info[1]
            sub_msg = info[1][2]

        await self.subgap_edit(check, message, msg = sub_msg)

    async def subgap_edit(self, channel, message, msg = None, embed = None):
        if msg:
            em = discord.Embed(color = discord.Color.blurple())
            em.add_field(name = "Leading Channel", value = msg)
            em.timestamp = datetime.datetime.utcnow()
        else:
            em = None

        message = await get_message(self.bot, channel, message)
        await message.edit(embed = em or embed)

    async def get_channel_info(self, first_ch, second_ch):
        base_uri = "https://www.googleapis.com/youtube/v3/channels"

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

        return ((first_name, first_count, sg), (second_name, second_count, sg))

    async def get_guild_sub(self, guild):
        youtuber = await self.bot.pool.fetchrow("SELECT first_ch, second_ch FROM sub_setup WHERE guildid = $1", guild)
        if youtuber is None:
            first_ch = "UC-lHJZR3Gqxm24_Vd_AJ5Yw"
            second_ch = "UCq-Fj5jknLsUf-MWSy4_brA"
        else:
            first_ch, second_ch = youtuber

        return (first_ch, second_ch)

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

        await ctx.send("What's the first channels name?")
        try:
            first_ch = await self.bot.wait_for("message", check = check, timeout = 30)
        except asyncio.TimeoutError:
            return

        first_search = await search(first_ch.content)

        if first_search["pageInfo"]["totalResults"] >= 1:
            first_ch = first_search["items"][0]["id"]["channelId"]
        else:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Channel Not Found", value = "Couldn't find a channel with that name.")
            await ctx.send(embed = em)
            return

        await ctx.send("What's the second channels name?")
        try:
            second_ch = await self.bot.wait_for("message", check = check, timeout = 30)
        except asyncio.TimeoutError:
            return

        second_search = await search(second_ch.content)

        if second_search["pageInfo"]["totalResults"] >= 1:
            second_ch = second_search["items"][0]["id"]["channelId"]
        else:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Channel Not Found", value = "Couldn't find a channel with that name.")
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

        guild_sub = await self.get_guild_sub(ctx.guild.id)
        info = await self.get_channel_info(*guild_sub)

        em = discord.Embed(color = discord.Color.blurple())
        em.add_field(name = "Leading Channel", value = info[0][2])
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
    async def subcount(self, ctx):
        guild_sub = await self.get_guild_sub(ctx.guild.id)
        info = await self.get_channel_info(*guild_sub)

        em = discord.Embed(color = discord.Color.red())
        em.add_field(name = info[0][0], value = f"{info[0][1]:,d}")
        em.add_field(name = info[1][0], value = f"{info[1][1]:,d}")
        em.add_field(name = "Leading Channel", value = info[0][2], inline = False)
        await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Subscribe(bot))