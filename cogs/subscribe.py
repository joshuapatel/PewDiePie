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
        self._sg = {}
        self.subgap_task.start() # pylint: disable=no-member

    def cog_unload(self):
        self.subgap_task.cancel() # pylint: disable=no-member

    @tasks.loop(seconds = 15)
    async def subgap_task(self):
        guilds = await self.bot.pool.fetch("SELECT * FROM subgap")
        self._sg.clear()

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

        if guild_sub[0] in self._sg:
            zn, zc = self._sg[guild_sub[0]]
        else:
            info = await self.get_channel_info(guild_sub[0])
            self._sg[guild_sub[0]] = info
            zn, zc = info

        if guild_sub[1] in self._sg:
            on, oc = self._sg[guild_sub[1]]
        else:
            info = await self.get_channel_info(guild_sub[1])
            self._sg[guild_sub[1]] = info
            on, oc = info

        if zc >= oc:
            sub_msg = f"{zn} is leading with {abs(zc - oc):,d} more subscribers than {on}"
        else:
            sub_msg = f"{on} is leading with {abs(zc - oc):,d} more subscribers than {zn}"

        await self.subgap_edit(check, message, msg = ((zn, zc), (on, oc), sub_msg))

    async def subgap_edit(self, channel, message, msg = None, embed = None):
        if msg:
            em = discord.Embed(color = discord.Color.blurple())
            em.add_field(name = msg[0][0], value = f"{msg[0][1]:,d}")
            em.add_field(name = msg[1][0], value = f"{msg[1][1]:,d}")
            em.add_field(name = "Leading Channel", value = msg[2], inline = False)
            em.timestamp = datetime.datetime.utcnow()
        else:
            em = None

        message = await get_message(self.bot, channel, message)
        await message.edit(embed = em or embed)

    async def get_channel_info(self, channel):
        base_uri = "https://www.googleapis.com/youtube/v3/channels"

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_uri}?part=snippet,contentDetails,statistics&id={channel}&key={config.ytdapi}") as ch:
                ch = await ch.json()

        ch_count = int(ch["items"][0]["statistics"]["subscriberCount"])

        ch_name = ch["items"][0]["snippet"]["title"]

        return (ch_name, ch_count)

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
        first_ch = await self.get_channel_info(guild_sub[0])
        second_ch = await self.get_channel_info(guild_sub[1])

        if first_ch[1] >= second_ch[1]:
            sub_msg = f"{first_ch[0]} is leading with {abs(first_ch[1] - second_ch[1]):,d} more subscribers than {second_ch[0]}"
        else:
            sub_msg = f"{second_ch[0]} is leading with {abs(first_ch[1] - second_ch[1]):,d} more subscribers than {first_ch[0]}"

        em = discord.Embed(color = discord.Color.blurple())
        em.add_field(name = first_ch[0], value = f"{first_ch[1]:,d}")
        em.add_field(name = second_ch[0], value = f"{second_ch[1]:,d}")
        em.add_field(name = "Leading Channel", value = sub_msg, inline = False)
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
        first_ch = await self.get_channel_info(guild_sub[0])
        second_ch = await self.get_channel_info(guild_sub[1])

        if first_ch[1] >= second_ch[1]:
            sub_msg = f"{first_ch[0]} is leading with {abs(first_ch[1] - second_ch[1]):,d} more subscribers than {second_ch[0]}"
        else:
            sub_msg = f"{second_ch[0]} is leading with {abs(first_ch[1] - second_ch[1]):,d} more subscribers than {first_ch[0]}"

        em = discord.Embed(color = discord.Color.red())
        em.add_field(name = first_ch[0], value = f"{first_ch[1]:,d}")
        em.add_field(name = second_ch[0], value = f"{second_ch[1]:,d}")
        em.add_field(name = "Leading Channel", value = sub_msg, inline = False)
        await ctx.send(embed = em)

    @commands.command(aliases = ["ci"])
    async def channelinfo(self, ctx, *, channel: str):
        async def search(ch_name):
            base_uri = "https://www.googleapis.com/youtube/v3/search"

            async with aiohttp.ClientSession() as session:
                async with session.get(f"{base_uri}?part=snippet&maxResults=1&q={ch_name}&type=channel&key={config.ytdapi}") as ch:
                    channel = await ch.json()

            return channel

        try:
            chid = search["items"][0]["id"]["channelId"]
        except TypeError:
            em = discord.Embed(color = discord.Color.red())
            em.add_field(name = "Channel Not Found", value = "Couldn't find a channel with that name.")
            await ctx.send(embed = em)
            return

        base_uri_id = "https://www.googleapis.com/youtube/v3/channels"
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_uri_id}?part=snippet,contentDetails,statistics&id={chid}&key={config.ytdapi}") as ch:
                ch = await ch.json()
            
        ch_count = int(ch["items"][0]["statistics"]["subscriberCount"])
        ch_name = ch["items"][0]["snippet"]["title"]
        ch_viewcount = int(ch["items"][0]["statistics"]["viewCount"])
        ch_vidcount = int(ch["items"][0]["statistics"]["videoCount"])
        ch_icon = str(ch["items"][0]["snippet"]["thumbnails"]["default"]["url"])

        em = discord.Embed(title = f"Info about {ch_name}", color = discord.Color.red())
        em.add_field(name = "Link", value = f"[Click Here](https://www.youtube.com/channel/{chid})")
        em.add_field(name = "Subcount", value = f"{ch_count:,d}")
        em.add_field(name = "Viewcount", value = f"{ch_viewcount:,d}")
        em.add_field(name = "Videocount", value = f"{ch_vidcount:,d}")
        em.set_thumbnail(url=ch_icon)
        await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Subscribe(bot))