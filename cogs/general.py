# -> Discord
import discord
from discord.ext import commands
# -> Loop
import asyncio
import aiohttp
# -> Miscellaneous
import random
import datetime
import textwrap
import secrets
# -> Configuration
import sys
sys.path.append("../")
import config


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bc_image = "<:bro_coin:541363630189576193>"
        self._8ball_responses = (
            "It is certain.",
            "Without a doubt.",
            "Yes - definitely.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Don't count on it.",
            "Outlook not so good.",
            "Very doubtful."
        )
            
    @commands.command()
    async def randomvid(self, ctx):
        await ctx.channel.trigger_typing()
        base = "https://www.googleapis.com/youtube/v3"
        apikey = config.ytdapi
        end = "&key=" + apikey
        pci = "UC-lHJZR3Gqxm24_Vd_AJ5Yw"
        tci = "UCq-Fj5jknLsUf-MWSy4_brA"

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"{base}/channels?part=snippet,contentDetails&id={tci}{end}") as tureq:
                tujson = await tureq.json()
            tupl = tujson["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            async with cs.get(f"{base}/playlistItems?playlistId={tupl}&maxResults=15&part=snippet,contentDetails{end}") as tuvids:
                tuvidsjson = await tuvids.json()

        tuvidslist = []
        vid = 0
        while vid < len(tuvidsjson["items"]):
            tvidid = tuvidsjson["items"][vid]["snippet"]["resourceId"]["videoId"]
            tuvidslist.append(tvidid)
            vid += 1

        async with aiohttp.ClientSession() as pcs:
            async with pcs.get(f"{base}/channels?part=snippet,contentDetails&id={pci}{end}") as pureq:
                pujson = await pureq.json()
            pupl = pujson["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            async with pcs.get(f"{base}/playlistItems?playlistId={pupl}&maxResults=15&part=snippet,contentDetails{end}") as puvids:
                puvidsjson = await puvids.json()

        puvidslist = []
        vid = 0
        while vid < len(puvidsjson["items"]):
            pvidid = puvidsjson["items"][vid]["snippet"]["resourceId"]["videoId"]
            puvidslist.append(pvidid)
            vid += 1

        ptuvidslist = tuvidslist + puvidslist
        rndptvids = random.choice(ptuvidslist)
        rndptvidsed = f"https://www.youtube.com/watch?v={rndptvids}"
        rndptvidthumb = f"https://img.youtube.com/vi/{rndptvids}/maxresdefault.jpg"

        em = discord.Embed(color = discord.Color.green())
        em.add_field(name = "YouTube Video", value = rndptvidsed)
        em.set_image(url = rndptvidthumb)
        await ctx.send(embed = em)

    @commands.command(aliases = ["yt"])
    async def youtube(self, ctx):
        em = discord.Embed(color = discord.Color.light_grey())
        em.add_field(name = "PewDiePie", value = "https://www.youtube.com/user/PewDiePie")
        em.add_field(name = "T-Series", value = "https://www.youtube.com/user/tseries")
        await ctx.send(embed = em)

    @commands.command(aliases = ["botinfo", "about", "support"])
    async def info(self, ctx):
        botlat = round(self.bot.latency * 1000, 3)

        em = discord.Embed(title = f"{self.bot.user.name} Information", color = discord.Color.green())
        em.add_field(name = "Bot Creator", value = self.bot.get_user(self.bot.owner_id) or "Multiple")
        em.add_field(name = "Bot Library", value = "discord.py rewrite")
        em.add_field(name = "Support Server", value = "https://discord.gg/we4DQ5u")
        em.add_field(name = "Bot Latency", value = f"{botlat} ms")
        em.add_field(name = "Server Count", value = f"{len(self.bot.guilds):,d} servers")
        em.add_field(name = "Vote", value = f"[Vote for me](https://discordbots.org/bot/{self.bot.user.id}/vote)")
        await ctx.send(embed = em)

    @commands.command()
    async def ping(self, ctx):
        botlat = round(self.bot.latency * 1000, 0)

        em = discord.Embed(title = "Pong!", description = f":ping_pong: `{botlat}ms`", color= discord.Color.red())
        await ctx.send(embed = em)

    @commands.command(aliases = ["vote"])
    async def invite(self, ctx):
        em = discord.Embed(color = discord.Color.orange())
        em.add_field(name = "Invite", value = f"[Invite me here!](https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=338717761)", inline = False)
        em.add_field(name = "Vote", value = f"[Vote for the bot](https://discordbots.org/bot/{self.bot.user.id}/vote)", inline = False)
        await ctx.send(embed = em)

    @commands.command(aliases = ["github", "gh"])
    async def source(self, ctx):
        await ctx.send("https://www.github.com/joshuapatel/PewDiePie")

    @commands.command(aliases = ["prefixtutorial", "tutprefix"])
    async def prefixtut(self, ctx):
        em = discord.Embed(color = discord.Color.dark_green())
        em.add_field(name = "Command Use", value = textwrap.dedent(f"""
        Sets the prefix for the current server. You must have the manage messages permission to use this command.
        **Set or change prefix**
        `p.setprefix [prefix here]`
        **Revert back to default prefix**
        `p.setprefix`
        **Show current prefix**
        `p.prefix` (does not require any special permissions to view)
        """))
        await ctx.send(embed = em)

    @commands.command(aliases = ["prefixes"])
    async def prefix(self, ctx):
        prefixes = self.bot.prefixes.get(ctx.guild.id)

        if prefixes is None:
            prefix = ""

            formatted = {p.lower() for p in self.bot.default_prefixes}

            for pf in formatted:
                prefix += pf + ", "

            prefix = prefix[:-2]
        else:
            prefix = prefixes

        em = discord.Embed(color = discord.Color.red())
        em.add_field(name = "Current Prefix", value = f"The current prefix for {self.bot.user.mention} is `{prefix}`")
        await ctx.send(embed = em)

    @commands.command(aliases = ["sprefix"])
    @commands.has_permissions(manage_messages = True)
    async def setprefix(self, ctx, *, prefix: str = None):
        if prefix is not None:
            if len(prefix) > 30:
                em = discord.Embed(color = discord.Color.dark_teal())
                em.add_field(name = "Prefix Character Limit Exceeded", value = "Prefixes can only be 30 characters or less")
                await ctx.send(embed = em)
                return

        gchck = await self.bot.pool.fetchrow("SELECT * FROM prefixes WHERE guildid = $1", ctx.guild.id)

        if gchck is None:
            if prefix is not None:
                await self.bot.pool.execute("INSERT INTO prefixes VALUES ($1, $2)", ctx.guild.id, prefix)

                em = discord.Embed(color = discord.Color.red())
                em.add_field(name = "Set Prefix", value = f"{self.bot.user.mention}'s prefix has been set to `{prefix}`")
                await ctx.send(embed = em)
            else:
                em = discord.Embed(color = discord.Color.dark_teal())
                em.add_field(name = "Error: Prefix Not Set", value = "Please specify a prefix to use")
                await ctx.send(embed = em)
                return
        else:
            if prefix is None:
                await self.bot.pool.execute("DELETE FROM prefixes WHERE guildid = $1", ctx.guild.id)

                em = discord.Embed(color = discord.Color.red())
                em.add_field(name = "Prefix Removed", value = f"{self.bot.user.mention}'s prefix has been set back to the default")
                await ctx.send(embed = em)
            else:
                await self.bot.pool.execute("UPDATE prefixes SET prefix = $1 WHERE guildid = $2", prefix, ctx.guild.id)

                em = discord.Embed(color = discord.Color.red())
                em.add_field(name = "Set Prefix", value = f"{self.bot.user.mention}'s prefix has been set to `{prefix}`")
                await ctx.send(embed = em)

        if prefix is not None:
            self.bot.prefixes[ctx.guild.id] = prefix
        else:
            self.bot.prefixes.pop(ctx.guild.id)

    @commands.command(aliases = ["memes"])
    async def meme(self, ctx):
        subreddit = ["memes", "meme", "dankmemes", "wholesomememes", "pewdiepiesubmissions"]
        subreddit = random.choice(subreddit)
        base = "https://www.reddit.com/r/" + subreddit

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base}/random.json") as response:
                j = await response.json()

        data = j[0]["data"]["children"][0]["data"]
        image_url = data["url"]
        title = data["title"]
        link = "https://www.reddit.com" + data["permalink"]
        upvotes = data["ups"]

        em = discord.Embed(title = title, url = link, color = discord.Color.red())
        em.set_image(url = image_url)
        em.set_footer(text = f"\N{THUMBS UP SIGN} {upvotes:,d}")
        em.timestamp = datetime.datetime.utcfromtimestamp(data["created_utc"])
        await ctx.send(embed = em)

    @commands.command()
    async def feedback(self, ctx, *, message: str):
        fbcheck = await self.bot.pool.fetchrow("SELECT * FROM fbblocked WHERE userid = $1", ctx.author.id)
        if fbcheck != None:
            blacklisted = discord.Embed(title = "Blacklisted", description = "You have been blacklisted from using the feedback command.", color = discord.Color.red())
            return await ctx.send(embed = blacklisted)

        em = discord.Embed(color = discord.Color.blue())
        em.add_field(name = "Feedback", value = f"""
        Your feedback for {self.bot.user.name} has been submitted
        If you abuse this command, you could lose your ability to send feedback.
        """)
        await ctx.send(embed = em)

        feedbackchannel = self.bot.get_channel(518603886483996683)
        emb = discord.Embed(title = "Feedback", color = discord.Color.blue())
        emb.set_thumbnail(url = ctx.author.avatar_url)
        emb.add_field(name = "User", value = str(ctx.author))
        emb.add_field(name = "User ID", value = str(ctx.author.id))
        emb.add_field(name = "Issue / Suggestion", value = message, inline = False)
        emb.add_field(name = "Guild Name", value = ctx.guild.name)
        emb.add_field(name = "Guild ID", value = str(ctx.guild.id))
        emb.timestamp = datetime.datetime.utcnow()

        await feedbackchannel.send(embed = emb)

    @commands.command()
    async def spoiler(self, ctx, *, spoiler: str):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        x = ""
        for b in spoiler:
            x += f"||{b}||"
        await ctx.send(x)

    @commands.command()
    async def joke(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://official-joke-api.appspot.com/random_joke') as r:
                raw = await r.json()
                embed = discord.Embed(title="Joke", description=f"{raw['setup']}\n\n{raw['punchline']}", color=discord.Color.red())
                await ctx.send(embed=embed)

    @commands.command()
    async def dadjoke(self, ctx):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get('https://icanhazdadjoke.com/', headers=headers) as r:
                raw = await r.json()
                embed = discord.Embed(title="Joke", description=f"{raw['joke']}", color=discord.Color.red())
                await ctx.send(embed=embed)

    @commands.command(name="8ball")
    @commands.guild_only()
    async def _8ball(self, ctx, *, question: str):
        await ctx.channel.trigger_typing()

        answer = random.choice(self._8ball_responses)
        em = discord.Embed(title = "8ball", color = discord.Color.red())
        em.add_field(name = "Question", value = question, inline = False)
        em.add_field(name = "Answer", value = answer, inline = False)
        await ctx.send(embed = em)

    @commands.command(aliases = ["ui", "whois"])
    @commands.guild_only()
    async def userinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        if user.activity is None:
            activity = None
        else:
            activity = user.activity.name

        roles = []

        if user.roles is None:
            roles.append("None")
        else:
            for role in user.roles:
                roles.append(role.name)

        try:
            coins, uses = await self.bot.pool.fetchrow("SELECT coins, uses FROM econ WHERE userid = $1 AND guildid = $2", user.id, ctx.guild.id)
        except TypeError:
            coins = uses = 0

        em = discord.Embed(title = f"Info about {user}", color = discord.Color.red())
        em.add_field(name = "Server Unique Name", value = user.nick)
        em.add_field(name = "Account Created", value = user.created_at.strftime("%m-%d-%Y"))
        em.add_field(name = "Joined Server",value = user.joined_at.strftime("%m-%d-%Y"))
        em.add_field(name = "ID", value = user.id)
        em.add_field(name = "Status", value = user.status)
        em.add_field(name = "Activity", value = activity)
        em.add_field(name = "Roles", value = ", ".join(roles))
        em.add_field(name = "Economy Info", value = f"**Bro Coins:** {coins:,d} {self.bc_image}\n**Economy Uses:** {uses:,d}")
        em.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed = em)

    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx):
        coins = await self.bot.pool.fetch("SELECT * FROM econ WHERE guildid = $1 ORDER BY coins DESC LIMIT 3", ctx.guild.id)
        coinstr = []
        if coins == []:
            coinstr.append("None")
        else:
            lbcount = 0
            for x in coins:
                lbcount += 1
                try:
                    uname = self.bot.get_user(x["userid"]).name
                    udiscrim = self.bot.get_user(x["userid"]).discriminator
                    complete = f"{uname}#{udiscrim}"
                except AttributeError:
                    complete = "User Not Found"

                if len(uname) > 17:
                    uname = uname[:-5] + "..."

                ucoins = format(x["coins"], ",d")
                coinstr.append(f"**{complete}:** {ucoins} {self.bc_image}")

        roles = []
        for role in ctx.guild.roles:
            roles.append(role.name)

        em = discord.Embed(title = f"Info about {ctx.guild.name}", color = discord.Color.red())
        em.add_field(name = "ID", value = ctx.guild.id)
        em.add_field(name = "Owner", value = f"{ctx.guild.owner.mention} ({ctx.guild.owner})")
        em.add_field(name = "Created At", value = ctx.guild.created_at.strftime("%m-%d-%Y"))
        em.add_field(name = "Region", value = ctx.guild.region)
        em.add_field(name = "Member Count", value = ctx.guild.member_count)
        em.add_field(name = "Roles", value = ", ".join(roles))
        em.add_field(name = "Top 3 Economy", value = "\n".join(coinstr))
        await ctx.send(embed = em)

    @commands.command()
    async def weather(self, ctx, *, cityname: str):
        owmapikey = await self.bot.pool.fetchval("SELECT openweathermap FROM apikeys")
        if owmapikey == None:
            await ctx.send("The OpenWeatherMap API key has not been set.")
            return

        citynamefinal = cityname.replace(" ", "%20")

        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://api.openweathermap.org/data/2.5/weather?appid={owmapikey}&q={citynamefinal}&units=imperial') as r:
                raw = await r.json()
                if raw['cod'] == "404":
                    em = discord.Embed(title = "City Not Found", description = "That city was not found.", color = discord.Color.red())
                    await ctx.send(embed = em)
                    return

                embed = discord.Embed(title = f"Weather for {raw['name']}", description = f"{raw['weather'][0]['main']} **|** {raw['weather'][0]['description']}", color = discord.Color.red())
                embed.add_field(name = "Coordinates", value = f"**Longitude:** {raw['coord']['lon']}, **Latitude:** {raw['coord']['lat']}")
                embed.add_field(name = "Country", value = raw['sys']['country'])
                embed.add_field(name = "Temperature", value = f"{raw['main']['temp']} °F (Min: {raw['main']['temp_min']} °F, Max: {raw['main']['temp_max']} °F)")
                embed.add_field(name = "Humidity", value = f"{raw['main']['humidity']}%")
                embed.add_field(name = "Wind Speed", value = f"{raw['wind']['speed']} MPH")
                embed.add_field(name = "Pressure", value = f"{raw['main']['pressure']}")
                await ctx.send(embed = embed)

    @commands.command()
    async def poll(self, ctx, *, polltext: str):
        nbytes = 7
        randomid = secrets.token_urlsafe(nbytes)
        try:
            embed = discord.Embed(title = "Poll", description = polltext, color = discord.Color.red())
            embed.set_footer(text = f"Created by {ctx.author} | To end the poll use +endpoll {randomid}")
            msg = await ctx.send(embed = embed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
            await self.bot.pool.execute("INSERT INTO polls VALUES ($1, $2, $3, $4, $5, $6)", ctx.guild.id, ctx.channel.id, msg.id, ctx.author.id, polltext, randomid)
        except discord.Forbidden:
            return

    @commands.command()
    async def endpoll(self, ctx, pollid: str):
        check = await self.bot.pool.fetchrow("SELECT * FROM polls WHERE guildid = $1 AND pollid = $2", ctx.guild.id, pollid)
        if check == None:
            return await ctx.send("I couldn't find a poll with that id in this guild.")

        if check["executorid"] != ctx.author.id:
            return await ctx.send("Only the Poll Creator can end that poll.")

        embed = discord.Embed(title = "Poll", description = "**POLL ENDED**", color = discord.Color.red())

        channel = self.bot.get_channel(check["channelid"])
        if channel == None:
            await self.bot.pool.execute("DELETE FROM polls WHERE guildid = $1 AND pollid = $2", ctx.guild.id, pollid)
            await ctx.send("I have ended that poll.")
            return

        msg = check["messageid"]

        pollmsg = await channel.fetch_message(msg)
        if pollmsg == None:
            await self.bot.pool.execute("DELETE FROM polls WHERE guildid = $1 AND pollid = $2", ctx.guild.id, pollid)
            await ctx.send("I have ended that poll.")
            return

        await pollmsg.edit(embed = embed)
        await self.bot.pool.execute("DELETE FROM polls WHERE guildid = $1 AND pollid = $2", ctx.guild.id, pollid)
        await ctx.send("I have ended that poll.")


def setup(bot):
    bot.add_cog(General(bot))