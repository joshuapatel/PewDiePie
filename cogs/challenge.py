import random
import discord
import json
import secrets
import aiohttp

from discord.ext import commands

class Challenge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command = True)
    @commands.is_owner()
    async def mchallenge(self, ctx):
        await ctx.send("**Options:** add, remove")

    @mchallenge.command()
    @commands.is_owner()
    async def add(self, ctx, type: str, *, text: str):
        if(type != "Easy" or "Medium" or "Hard"):
            return await ctx.send("That is not a valid challenge type.")

        check = await self.bot.pool.fetchrow("SELECT * FROM challenges WHERE challengename = $1", text)

        if check != None:
            return await ctx.send("That challenge is already in the database.")
        
        await self.bot.pool.execute("INSERT INTO challenges VALUES ($1, $2)", text, type)
        em = discord.Embed(title = "Challenge", description = "Challenge Added!", color = discord.Color.red())
        await ctx.send(embed = em)

    @mchallenge.command()
    @commands.is_owner()
    async def remove(self, ctx, cid: int):
        check = await self.bot.pool.fetchrow("SELECT * FROM challenges WHERE challengeid = $1", cid)

        if check == None:
            return await ctx.send("That challenge is not in the database.")
        
        await self.bot.pool.execute("DELETE FROM challenges WHERE challengeid = $1", cid)
        em = discord.Embed(title = "Challenge", description = "Challenge Removed.", color = discord.Color.red())
        await ctx.send(embed = em)

    @commands.group(invoke_without_command = True)
    async def challenge(self, ctx):
        challenges = await self.bot.pool.fetch("SELECT challengename, challengeid FROM challenges")

        try:
            challenges = random.choice(challenges)
        except IndexError:
            return await ctx.send("There aren't any challenges in the database.")

        ctext = challenges['challengename']
        ctype = challenges['challengetype']
        cid = challenges['challengeid']

        em = discord.Embed(title = f"Challenge #{cid}", description = f"**{ctype}:** {ctext}", color = discord.Color.red())
        await ctx.send(embed = em)

    @challenge.command()
    async def easy(self, ctx):
        challenges = await self.bot.pool.fetch("SELECT challengename, challengeid FROM challenges WHERE challengetype = $1", "Easy")

        try:
            challenges = random.choice(challenges)
        except IndexError:
            return await ctx.send("There aren't any easy challenges in the database.")

        ctext = challenges['challengename']
        ctype = challenges['challengetype']
        cid = challenges['challengeid']

        em = discord.Embed(title = f"Challenge #{cid}", description = f"**{ctype}:** {ctext}", color = discord.Color.red())
        await ctx.send(embed = em)

    @challenge.command()
    async def medium(self, ctx):
        challenges = await self.bot.pool.fetch("SELECT challengename, challengeid FROM challenges WHERE challengetype = $1", "Medium")

        try:
            challenges = random.choice(challenges)
        except IndexError:
            return await ctx.send("There aren't any medium challenges in the database.")

        ctext = challenges['challengename']
        ctype = challenges['challengetype']
        cid = challenges['challengeid']

        em = discord.Embed(title = f"Challenge #{cid}", description = f"**{ctype}:** {ctext}", color = discord.Color.red())
        await ctx.send(embed = em)

    @challenge.command()
    async def hard(self, ctx):
        challenges = await self.bot.pool.fetch("SELECT challengename, challengeid FROM challenges WHERE challengetype = $1", "Hard")

        try:
            challenges = random.choice(challenges)
        except IndexError:
            return await ctx.send("There aren't any hard challenges in the database.")

        ctext = challenges['challengename']
        ctype = challenges['challengetype']
        cid = challenges['challengeid']

        em = discord.Embed(title = f"Challenge #{cid}", description = f"**{ctype}:** {ctext}", color = discord.Color.red())
        await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Challenge(bot))