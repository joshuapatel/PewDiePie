import discord
from discord.ext import commands
import random


class EconomyCrime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tcoinimage = "<:bro_coin:541363630189576193>"

    async def crime_cache(self):
        self.bot.econ["crime"] = {}
        self.bot.econ["crime"]["pos"] = await self.bot.pool.fetch("SELECT name, id FROM crime WHERE fate = true")
        self.bot.econ["crime"]["neg"] = await self.bot.pool.fetch("SELECT name, id FROM crime WHERE fate = false")

    async def cad_user(ctx): # pylint: disable=no-self-argument
        # pylint: disable=E1101
        economy = ctx.bot.get_cog("Economy")

        if not ctx.guild.id in ctx.bot.econ["users"]["guildid"]:
            ctx.bot.econ["users"]["guildid"][ctx.guild.id] = {}

        dc = ctx.bot.econ["users"]["guildid"][ctx.guild.id]

        if ctx.author.id in dc:
            return True
        else:
            await ctx.bot.pool.execute("INSERT INTO econ VALUES ($1, $2, $3)", 0, ctx.author.id, ctx.guild.id)
            await economy.up_usercache(ctx.guild.id, ctx.author.id)
            return True

        return False
        # pylint: enable=E1101

    @commands.command()
    @commands.check(cad_user)
    @commands.cooldown(5, 10, commands.BucketType.member)
    async def crime(self, ctx):
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

        phrases["name"] = phrases["name"].replace("{ctg}", f"{ctg:,d}").replace("{tcoinimage}", self.tcoinimage)

        if fate:
            em = discord.Embed(color = discord.Color.green())
        else:
            em = discord.Embed(color = discord.Color.red())

        em.add_field(name = "Crime", value = phrases["name"])
        em.set_footer(text = f"Phrase #{phrases['id']:,d}")
        await ctx.send(embed = em)

        await self.bot.pool.execute("UPDATE econ SET coins = coins + $1 WHERE userid = $2 AND guildid = $3", ctg, ctx.author.id, ctx.guild.id)
        await self.bot.pool.execute("UPDATE econ SET uses = uses + 1 WHERE userid = $1 AND guildid = $2", ctx.author.id, ctx.guild.id)


def setup(bot):
    bot.loop.create_task(EconomyCrime(bot).crime_cache())
    bot.add_cog(EconomyCrime(bot))