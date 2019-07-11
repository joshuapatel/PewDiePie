# -> Discord
import discord
from discord.ext import commands
# -> Miscellaneous
import random
import datetime
import humanize
# -> Loop
import asyncio


class AmountConverter(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            return int(argument)
        except:
            pass
        if "all" in argument:
            coins = await ctx.bot.pool.fetchval("SELECT coins FROM econ WHERE userid = $1 AND guildid = $2", ctx.author.id, ctx.guild.id)
            if ctx.command.name == "transfer":
                coins = round(coins * 0.5)
            return coins
        elif "," in argument:
            return int(argument.replace(",", ""))
        else:
            return 0

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bc_image = "<:bro_coin:541363630189576193>"
        self._mc = set()
        self.bot.loop.create_task(self.cache())

    async def cache(self):
        users = await self.bot.pool.fetch("SELECT guildid, userid FROM econ")
        self._mc.add(f"{u[0]}:{u[1]}" for u in users)

        # Shovel
        self.bot.econ["pos"] = await self.bot.pool.fetch("SELECT name, id FROM shovel WHERE fate = true")
        self.bot.econ["neg"] = await self.bot.pool.fetch("SELECT name, id FROM shovel WHERE fate = false")
        # Crime
        self.bot.econ["crime"] = {}
        self.bot.econ["crime"]["pos"] = await self.bot.pool.fetch("SELECT name, id FROM crime WHERE fate = true")
        self.bot.econ["crime"]["neg"] = await self.bot.pool.fetch("SELECT name, id FROM crime WHERE fate = false")

    async def cog_before_invoke(self, ctx):
        dc = f"{ctx.guild.id}:{ctx.author.id}" in self._mc

        if not dc:
            await self.bot.pool.execute("INSERT INTO econ VALUES ($1, $2, $3)", 0, ctx.author.id, ctx.guild.id)
            self._mc.add(f"{ctx.guild.id}:{ctx.author.id}")

    @commands.command(aliases = ["shove;", "shove", "shv", "sh", "work"])
    @commands.cooldown(5, 10, commands.BucketType.member)
    async def shovel(self, ctx):
        """You work all day shoveling for Bro Coins"""
        fate = random.choice([True, False, True, False, True])

        if fate:
            ctg = random.randint(1, 1500)
            phrases = self.bot.econ["pos"]
        else:
            ctg = -random.randint(1, 700)
            phrases = self.bot.econ["neg"]

        try:
            phrases = random.choice(phrases)
        except IndexError:
            phrases = {"id": 1, "name": "You need {ctg} {tcoinimage} to add shovel phrases."}

        message = phrases["name"].replace("{ctg}", f"{ctg:,d}").replace("{tcoinimage}", self.bc_image)

        if fate:
            em = discord.Embed(color = discord.Color.green())
        else:
            em = discord.Embed(color = discord.Color.red())

        em.add_field(name = "Shovel", value = message)
        em.set_footer(text = f"Phrase #{phrases['id']:,d}")
        await ctx.send(embed = em)

        await self.bot.pool.execute("UPDATE econ SET coins = coins + $1 WHERE userid = $2 AND guildid = $3", ctg, ctx.author.id, ctx.guild.id)
        await self.bot.pool.execute("UPDATE econ SET uses = uses + 1 WHERE userid = $1 AND guildid = $2", ctx.author.id, ctx.guild.id)

    @commands.command()
    @commands.cooldown(5, 10, commands.BucketType.member)
    async def crime(self, ctx):
        """You commit a crime and gain or lose coins based on your success"""
        fate = random.choice([True, False, True, False, True, False, False])

        if fate:
            ctg = random.randint(1, 1500)
            phrases = self.bot.econ["crime"]["pos"]
        else:
            ctg = -random.randint(1, 700)
            phrases = self.bot.econ["crime"]["neg"]

        try:
            phrases = random.choice(phrases)
        except IndexError:
            phrases = {"id": 1, "name": "You need {ctg} {tcoinimage} to add crime phrases."}

        message = phrases["name"].replace("{ctg}", f"{ctg:,d}").replace("{tcoinimage}", self.bc_image)

        if fate:
            em = discord.Embed(color = discord.Color.green())
        else:
            em = discord.Embed(color = discord.Color.red())

        em.add_field(name = "Crime", value = message)
        em.set_footer(text = f"Phrase #{phrases['id']:,d}")
        await ctx.send(embed = em)

        await self.bot.pool.execute("UPDATE econ SET coins = coins + $1 WHERE userid = $2 AND guildid = $3", ctg, ctx.author.id, ctx.guild.id)
        await self.bot.pool.execute("UPDATE econ SET uses = uses + 1 WHERE userid = $1 AND guildid = $2", ctx.author.id, ctx.guild.id)

    @commands.command()
    async def daily(self, ctx):
        """Daily bonus of Bro Coins"""
        time = await self.bot.pool.fetchval("SELECT time FROM daily WHERE userid = $1 AND guildid = $2", ctx.author.id, ctx.guild.id)
        now = datetime.datetime.utcnow()
        tomorrow = now + datetime.timedelta(days=1)

        if time is not None and time > now:
            human_time = humanize.naturaldelta(time - now)

            em = discord.Embed(color=discord.Color.dark_teal())
            em.add_field(name="Daily Cooldown", value=f"You must wait {human_time} until you can cash in your daily bonus.")
            await ctx.send(embed=em)
            return

        check = await self.bot.pool.fetchval("SELECT level FROM donator WHERE userid = $1", ctx.author.id)
        if not check:
            ctg = random.randint(4500, 10000)

        if check == 1:
            ctg = random.randint(5625, 12500)

        if check == 2:
            ctg = random.randint(6750, 15000)

        em = discord.Embed(color=discord.Colour.green())
        em.add_field(name="Daily", value=f"You cashed in your daily bonus of {ctg:,d} {self.bc_image}")
        await ctx.send(embed=em)

        if time is None:
            await self.bot.pool.execute("INSERT INTO daily VALUES ($1, $2, $3)", ctx.author.id, ctx.guild.id, tomorrow)
        else:
            await self.bot.pool.execute("UPDATE daily SET time = $1 WHERE userid = $2 AND guildid = $3", tomorrow, ctx.author.id, ctx.guild.id)

        await self.bot.pool.execute("UPDATE econ SET coins = coins + $1 WHERE userid = $2 AND guildid = $3", ctg, ctx.author.id, ctx.guild.id)

    @commands.command(aliases = ["give", "givemoney", "send", "sendmoney", "add", "addmoney"])
    async def pay(self, ctx, amount: AmountConverter, *, user: discord.Member):
        """Pays a user with a specified amount of Bro Coins"""
        if 0 >= amount:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Too Small", value = f"You cannot send {self.bc_image} that is 0 or smaller")
            await ctx.send(embed = em)
            return

        aucash = await self.bot.pool.fetchval("SELECT coins FROM econ WHERE userid = $1 AND guildid = $2", ctx.author.id, ctx.guild.id)
        if aucash >= amount:
            repcheck = await self.bot.pool.fetchrow("SELECT * FROM econ WHERE userid = $1 AND guildid = $2", user.id, ctx.guild.id)
            if repcheck is None:
                await self.bot.pool.execute("INSERT INTO econ VALUES ($1, $2, $3)", 0, user.id, ctx.guild.id)

            await self.bot.pool.execute("UPDATE econ SET coins = coins + $1 WHERE userid = $2 AND guildid = $3", amount, user.id, ctx.guild.id)
            await self.bot.pool.execute("UPDATE econ SET coins = coins - $1 WHERE userid = $2 AND guildid = $3", amount, ctx.author.id, ctx.guild.id)

            em = discord.Embed(color = discord.Color.dark_green())
            em.add_field(name = f"Sent Bro Coin to {user.name}#{user.discriminator}", value = f"{amount:,d} {self.bc_image} was sent to {user.mention}")
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = em)
        else:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Not Enough", value = f"You do not have enough {self.bc_image} to send {amount:,d}")
            await ctx.send(embed = em)

    @commands.command(aliases = ["bal", "money", "cash", "$", "coins", "coin", "bank"])
    async def balance(self, ctx, *, user: discord.Member = None):
        """Shows the users balance and economy uses"""
        if user is None:
            user = ctx.author

        try:
            coins, uses = await self.bot.pool.fetchrow("SELECT coins, uses FROM econ WHERE userid = $1 AND guildid = $2", user.id, ctx.guild.id)
        except TypeError:
            coins = uses = 0

        if uses == 1:
            u = "use"
        else:
            u = "uses"

        em = discord.Embed(color=discord.Color.blue())
        em.set_author(name=user, icon_url=user.avatar_url)
        em.add_field(name="Bro Coins", value=f"{coins:,d} {self.bc_image}")
        em.add_field(name="Economy Uses", value=f"{uses:,d} {u}")
        await ctx.send(embed=em)

    @commands.command(aliases = ["lb", "lead", "board", "leadboard"])
    async def leaderboard(self, ctx, param: str = ""):
        """Shows the leaderboard for Bro Coins"""
        if param.lower() in ["server", "guild"]:
            coins = await self.bot.pool.fetch("SELECT * FROM econ WHERE guildid = $1 ORDER BY coins DESC LIMIT 5", ctx.guild.id)
        else:
            coins = await self.bot.pool.fetch("SELECT * FROM econ ORDER BY coins DESC LIMIT 5")

        em = discord.Embed(color = discord.Color.dark_red())

        if coins == []:
            em.add_field(name = "Leaderboard", value = "No one is using Bro Coin so there is nothing on the leaderboard")
        else:
            if param.lower() in ["server", "guild"]:
                em.set_author(name = f"{ctx.guild.name}'s Leaderboard")
            else:
                em.set_author(name = "Leaderboard")

        lbcount = 0
        for x in coins:
            lbcount += 1
            try:
                uname = self.bot.get_user(x["userid"]).name
            except AttributeError:
                uname = "User Not Found"
            try:
                gname = self.bot.get_guild(x["guildid"]).name
            except AttributeError:
                gname = "Guild Not Found"
            if len(uname) > 17:
                uname = uname[:-5] + "..."
            if len(gname) > 20:
                gname = gname[:-7] + "..."

            coins = format(x["coins"], ",d")
            uses = format(x["uses"], ",d")

            em.add_field(name = f"#{lbcount} - {uname} ({gname})", value = f"Bro Coins: {coins} {self.bc_image}\nShovel Uses: {uses}", inline = False)

        prefix = ctx.prefix.replace(self.bot.user.mention, f"@{self.bot.user.name}")
        em.set_footer(text = f"PROTIP: Use {prefix}shovel to collect Bro Coins")
        await ctx.send(embed = em)

    @commands.command(aliases = ["bet", "ontheline", "bets", "dice", "die"])
    @commands.cooldown(1, 60, commands.BucketType.member)
    async def gamble(self, ctx, amount: AmountConverter = 5000):
        """Gambles a specific amount of Bro Coins"""
        usercoins = await self.bot.pool.fetchval("SELECT coins FROM econ WHERE userid = $1 AND guildid = $2", ctx.author.id, ctx.guild.id)
        if 0 >= amount:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Too Small", value = f"You cannot gamble {self.bc_image} that is 0 or smaller")
            await ctx.send(embed = em)
            self.bot.get_command("gamble").reset_cooldown(ctx)
            return

        if usercoins >= amount:
            choice = random.choice([True, False, False, True, False])
            if choice:
                cm = "Gained"
            else:
                cm = "Lost"
                amount = -amount

            await self.bot.pool.execute("UPDATE econ SET coins = coins + $1 WHERE userid = $2 AND guildid = $3", amount, ctx.author.id, ctx.guild.id)

            em = discord.Embed(color = discord.Color.dark_red())
            em.add_field(name = f"You {cm} Coins", value = f"You have {cm.lower()} {amount:,d} {self.bc_image} from the gamble")
            await ctx.send(embed = em)
        else:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Not Enough", value = f"You do not have {amount:,d} {self.bc_image} to gamble")
            await ctx.send(embed = em)

            self.bot.get_command("gamble").reset_cooldown(ctx)

    @commands.command(aliases = ["rob", "take", "thief", "steel", "theft", "thieves"])
    @commands.cooldown(1, 7200, commands.BucketType.member)
    async def steal(self, ctx, *, user: discord.Member):
        """Steals from a user"""
        if user.bot:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Cannot Steal", value = "You cannot steal from bots")
            await ctx.send(embed = em)
            return
        if user.id == ctx.author.id:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Cannot Steal", value = "You cannot steal from yourself")
            await ctx.send(embed = em)
            self.bot.get_command("steal").reset_cooldown(ctx)
            return

        mu = await self.bot.pool.fetchval("SELECT coins FROM econ WHERE userid = $1 AND guildid = $2", user.id, ctx.guild.id)
        if mu is None:
            mu = 0

        coinchance = random.choice([True, False, True, True, False, False])
        if coinchance:
            giveper = random.randint(1, 5)
            give = round(mu * float(f"0.0{giveper}"))

            if 0 >= give:
                em = discord.Embed(color = discord.Color.dark_teal())
                em.add_field(name = "Not Enough", value = f"{user.mention} does not have enough coins to steal from")
                await ctx.send(embed = em)
                self.bot.get_command("steal").reset_cooldown(ctx)
                return

            await self.bot.pool.execute("UPDATE econ SET coins = coins - $1 WHERE userid = $2 AND guildid = $3", give, user.id, ctx.guild.id)
            await self.bot.pool.execute("UPDATE econ SET coins = coins + $1 WHERE userid = $2 AND guildid = $3", give, ctx.author.id, ctx.guild.id)

            em = discord.Embed(color = discord.Color.dark_red())
            em.add_field(name = f"Stole from {user.name}", value = f"You stole {give:,d} {self.bc_image} from {user.mention}")
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = em)
        else:
            em = discord.Embed(color = discord.Color.dark_red())
            em.add_field(name = "Caught by the Police", value = f"Looks like this time {user.mention} got off the hook since the police showed up")
            await ctx.send(embed = em)

    @commands.command()
    async def transfer(self, ctx, amount: AmountConverter, *, guild: str):
        """Sends Bro Coins to another server. The max amount is 50% of your coins."""
        if 0 >= amount:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Too Small", value = f"You cannot transfer {self.bc_image} that is 0 or smaller")
            await ctx.send(embed = em)
            return

        guild = discord.utils.get(self.bot.guilds, name = guild)
        if guild is None:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Guild Not Found", value = f"{self.bot.user.name} could not find the guild")
            await ctx.send(embed = em)
            return

        transfercheck = await self.bot.pool.fetchval("SELECT transfer FROM econ WHERE userid = $1 AND guildid = $2", ctx.author.id, ctx.guild.id)
        if transfercheck:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Already Transferred", value = "You have already transferred your Bro Coins from this guild")
            await ctx.send(embed = em)
            return

        coins = await self.bot.pool.fetchval("SELECT coins FROM econ WHERE userid = $1 AND guildid = $2", ctx.author.id, ctx.guild.id)
        coins = round(coins * 0.5)

        if coins >= amount:
            gc = await self.bot.pool.fetchrow("SELECT * FROM econ WHERE userid = $1 AND guildid = $2", ctx.author.id, guild.id)
            if gc is None:
                await self.bot.pool.execute("INSERT INTO econ VALUES ($1, $2, $3)", amount, ctx.author.id, guild.id)
            else:
                await self.bot.pool.execute("UPDATE econ SET coins = coins + $1 WHERE userid = $2 AND guildid = $3", amount, ctx.author.id, guild.id)

            await self.bot.pool.execute("UPDATE econ SET transfer = true WHERE userid = $1 AND guildid = $2", ctx.author.id, ctx.guild.id)
            await self.bot.pool.execute("UPDATE econ SET coins = coins - $1 WHERE userid = $2 AND guildid = $3", amount, ctx.author.id, ctx.guild.id)

            em = discord.Embed(color = discord.Color.dark_red())
            em.add_field(name = "Bro Coins Transferred", value = f"{amount:,d} {self.bc_image} has been transferred to `{guild.name}`")
            em.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = em)
        else:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Not Enough", value = f"You do not have enough Bro Coins to transfer {amount:,d} {self.bc_image} to `{guild.name}`")
            em.set_footer(text = "NOTE: You are only able to transfer up to 50% of your Bro Coins")
            await ctx.send(embed = em)

    @commands.command(aliases = ["stats", "stat"])
    async def statistics(self, ctx):
        """Shows statistics on Bro Coin usage"""
        econ_info = await self.bot.pool.fetchrow("SELECT COUNT(coins), AVG(coins), SUM(coins) FROM econ")

        tcusbcount = econ_info["count"]
        tcavg = econ_info["avg"]
        tcall = econ_info["sum"]

        tcsuses = await self.bot.pool.fetchval("SELECT SUM(uses) FROM econ")
        if tcsuses == 1:
            u = "use"
        else:
            u = "uses"

        tlu = await self.bot.pool.fetchrow("SELECT userid, coins FROM econ ORDER BY coins DESC LIMIT 1")
        spc = await self.bot.pool.fetchval("SELECT COUNT(name) FROM shovel")
        ft = await self.bot.pool.fetchval("SELECT COUNT(*) FROM shovel WHERE fate = true")
        ff = await self.bot.pool.fetchval("SELECT COUNT(*) FROM shovel WHERE fate = false")

        tluname = self.bot.get_user(tlu["userid"])
        if tluname is None:
            tluname = "User Not Found"

        em = discord.Embed(color = discord.Color.red())
        em.set_author(name = "Bro Coin Statistics")
        em.add_field(name = "Accounts", value = f"{tcusbcount:,d} accounts")
        em.add_field(name = "Average Amount", value = f"{round(tcavg):,d} {self.bc_image}")
        em.add_field(name = "Total Amount", value = f"{round(tcall):,d} {self.bc_image}")
        em.add_field(name = "Leading User", value = f"{tluname}")
        em.add_field(name = "Leading User Amount", value = f"{tlu['coins']:,d} {self.bc_image}")
        em.add_field(name = "Shovel Phrases", value = f"{spc:,d} phrases")
        em.add_field(name = "Shovel Uses", value = f"{round(tcsuses):,d} {u}")
        em.add_field(name = "Positive Phrases", value = f"{ft:,d} phrases")
        em.add_field(name = "Negative Phrases", value = f"{ff:,d} phrases")

        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Economy(bot))