import discord
from discord.ext import commands
import random


class EconomyCrime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tcoinimage = "<:bro_coin:541363630189576193>"
        self.bot.loop.create_task(self.crime_cache())

    async def crime_cache(self):
        self.bot.econ["crime"] = {}
        self.bot.econ["crime"]["pos"] = await self.bot.pool.fetch("SELECT name, id FROM crime WHERE fate = true")
        self.bot.econ["crime"]["neg"] = await self.bot.pool.fetch("SELECT name, id FROM crime WHERE fate = false")

    async def cad_user(ctx): # pylint: disable=no-self-argument
        # pylint: disable=E1101
        dc = await ctx.bot.redis.sismember("econ_users", f"{ctx.guild.id}:{ctx.author.id}")

        if not dc:
            await ctx.bot.pool.execute("INSERT INTO econ VALUES ($1, $2, $3)", 0, ctx.author.id, ctx.guild.id)
            await ctx.bot.redis.sadd("econ_users", f"{ctx.guild.id}:{ctx.author.id}")
            return True

        return True
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

        message = phrases["name"].replace("{ctg}", f"{ctg:,d}").replace("{tcoinimage}", self.tcoinimage)

        if fate:
            em = discord.Embed(color = discord.Color.green())
        else:
            em = discord.Embed(color = discord.Color.red())

        em.add_field(name = "Crime", value = message)
        em.set_footer(text = f"Phrase #{phrases['id']:,d}")
        await ctx.send(embed = em)

        await self.bot.pool.execute("UPDATE econ SET coins = coins + $1 WHERE userid = $2 AND guildid = $3", ctg, ctx.author.id, ctx.guild.id)
        await self.bot.pool.execute("UPDATE econ SET uses = uses + 1 WHERE userid = $1 AND guildid = $2", ctx.author.id, ctx.guild.id)


def setup(bot):
    bot.add_cog(EconomyCrime(bot))