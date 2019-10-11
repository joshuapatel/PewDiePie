import discord
from discord.ext import commands


class EconomyPhrases(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_shovel(self):
        self.bot.econ["pos"] = await self.bot.pool.fetch("SELECT name, id FROM shovel WHERE fate = true")
        self.bot.econ["neg"] = await self.bot.pool.fetch("SELECT name, id FROM shovel WHERE fate = false")

    async def update_crime(self):
        self.bot.econ["crime"]["pos"] = await self.bot.pool.fetch("SELECT name, id FROM crime WHERE fate = true")
        self.bot.econ["crime"]["neg"] = await self.bot.pool.fetch("SELECT name, id FROM crime WHERE fate = false")

    @commands.group(invoke_without_command = True)
    async def phrase(self, ctx, pid: int, u: str = "shovel"):
        if "crime" in u:
            table = "crime"
        else:
            table = "shovel"

        pcheck = await self.bot.pool.fetchrow(f"SELECT name, fate FROM {table} WHERE id = $1", pid)
        if pcheck == None:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Phrase Not Found", value = f"Phrase #{pid} could not be found")
            await ctx.send(embed = em)
            return

        fate = pcheck["fate"]
        p = pcheck["name"]

        if fate:
            em = discord.Embed(color = discord.Color.green())
        else:
            em = discord.Embed(color = discord.Color.red())

        em.add_field(name = "Raw Phrase", value = p)
        em.set_footer(text = f"Phrase #{pid}")
        await ctx.send(embed = em)

    @phrase.command()
    @commands.is_owner()
    async def add(self, ctx, fate: bool, *, phrase: str):
        if phrase.startswith("<-- ADD CRIME -->"):
            phrase = phrase.replace("<-- ADD CRIME -->", "")
            table = "crime"
        else:
            table = "shovel"

        await self.bot.pool.execute(f"INSERT INTO {table} VALUES ($1, $2)", phrase, fate)
        pid = await self.bot.pool.fetchval(f"SELECT id FROM {table} WHERE name = $1 AND fate = $2", phrase, fate)

        if fate:
            em = discord.Embed(color = discord.Color.green())
        else:
            em = discord.Embed(color = discord.Color.red())

        em.add_field(name = "Added Phrase", value = f"The phrase has been added to the {table} command. Fate: {fate}")
        em.set_footer(text = f"Phrase #{pid}")
        await ctx.send(embed = em)

        if table == "shovel":
            await self.update_shovel()
        else:
            await self.update_crime()

    @phrase.command()
    @commands.is_owner()
    async def edit(self, ctx, pid: int, *, phrase: str):
        if phrase.startswith("<-- EDIT CRIME -->"):
            phrase = phrase.replace("<-- EDIT CRIME -->", "")
            table = "crime"
        else:
            table = "shovel"

        pcheck = await self.bot.pool.fetchrow(f"SELECT * FROM {table} WHERE id = $1", pid)
        if pcheck == None:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Phrase Not Found", value = f"Phrase #{pid} could not be found")
            await ctx.send(embed = em)
            return

        await self.bot.pool.execute(f"UPDATE {table} SET name = $1 WHERE id = $2", phrase, pid)

        em = discord.Embed(color = discord.Color.dark_red())
        em.add_field(name = "Phrase Updated", value = f"Phrase #{pid} has been updated")
        await ctx.send(embed = em)

        if table == "shovel":
            await self.update_shovel()
        else:
            await self.update_crime()

    @phrase.command(aliases = ["remove"])
    @commands.is_owner()
    async def delete(self, ctx, pid: int, crime: bool = False):
        if crime:
            table = "crime"
        else:
            table = "shovel"

        pcheck = await self.bot.pool.fetchrow(f"SELECT * FROM {table} WHERE id = $1", pid)
        if pcheck == None:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Phrase Not Found", value = f"Phrase #{pid} could not be found")
            await ctx.send(embed = em)
            return

        await self.bot.pool.execute(f"DELETE FROM {table} WHERE id = $1", pid)

        em = discord.Embed(color = discord.Color.dark_red())
        em.add_field(name = "Phrase Removed", value = f"Phrase #{pid} has been removed")
        await ctx.send(embed = em)

        if table == "shovel":
            await self.update_shovel()
        else:
            await self.update_crime()

    @commands.group(invoke_without_command = True)
    async def crimephrase(self, ctx, pid: int):
        await ctx.invoke(self.bot.get_command("phrase"), pid = pid, u = "crime")

    @crimephrase.command(name = "add")
    @commands.is_owner()
    async def crime_add(self, ctx, fate: bool, *, phrase: str):
        phrase = "<-- ADD CRIME -->" + phrase
        await ctx.invoke(self.bot.get_command("phrase add"), fate = fate, phrase = phrase)

    @crimephrase.command(name = "edit")
    @commands.is_owner()
    async def crime_edit(self, ctx, pid: int, *, phrase: str):
        phrase = "<-- EDIT CRIME -->" + phrase
        await ctx.invoke(self.bot.get_command("phrase edit"), pid = pid, phrase = phrase)

    @crimephrase.command(name = "delete", aliases = ["remove"])
    @commands.is_owner()
    async def crime_delete(self, ctx, pid: int):
        await ctx.invoke(self.bot.get_command("phrase delete"), pid = pid, crime = True)


def setup(bot):
    bot.add_cog(EconomyPhrases(bot))