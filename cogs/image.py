# -> Discord
import discord
from discord.ext import commands

import aiohttp

import struct
import io
import contextlib
from io import BytesIO


class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def imggenembed(self, ctx, title: str, imgurl: str):
        em = discord.Embed(title = title, color = discord.Color.red())
        em.set_image(url=imgurl)
        em.set_footer(text="NOTE: These commands are still in beta.")
        await ctx.send(embed = em)

    @commands.command()
    async def changemymind(self, ctx, *, text: str):
        check = await self.bot.pool.fetchval("SELECT level FROM donator WHERE userid = $1", ctx.author.id)
        if not check:
            em = discord.Embed(color=discord.Color.dark_teal())
            em.add_field(name="Donator Command", value=f"This is a patreon only command. To become a supporter, go [here](https://patreon.com/pdpbot).")
            await ctx.send(embed=em)
            return

        await ctx.channel.trigger_typing()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://nekobot.xyz/api/imagegen?type=changemymind&text={text}'.replace(" ", "%20"), headers=headers) as r:
                raw = await r.json()
                img = raw['message']
                await self.imggenembed(ctx, "Change My Mind", img)

    @commands.command()
    async def trumptweet(self, ctx, *, text: str):
        check = await self.bot.pool.fetchval("SELECT level FROM donator WHERE userid = $1", ctx.author.id)
        if not check:
            em = discord.Embed(color=discord.Color.dark_teal())
            em.add_field(name="Donator Command", value=f"This is a patreon only command. To become a supporter, go [here](https://patreon.com/pdpbot).")
            await ctx.send(embed=em)
            return

        await ctx.channel.trigger_typing()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}'.replace(" ", "%20"), headers=headers) as r:
                raw = await r.json()
                img = raw['message']
                await self.imggenembed(ctx, "Trump Tweet", img)

    @commands.command()
    async def triggered(self, ctx, user: discord.Member = None):
        check = await self.bot.pool.fetchval("SELECT level FROM donator WHERE userid = $1", ctx.author.id)
        if not check:
            em = discord.Embed(color=discord.Color.dark_teal())
            em.add_field(name="Donator Command", value=f"This is a patreon only command. To become a supporter, go [here](https://patreon.com/pdpbot).")
            await ctx.send(embed=em)
            return
            
        if user == None:
            user = ctx.author

        dmapikey = await self.bot.pool.fetchval("SELECT key FROM apikeys WHERE name = $1", "dankmemer")
        if dmapikey == None:
            await ctx.send("The Dank Memer API key has not been set.")
            return

        await ctx.channel.trigger_typing()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": dmapikey
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://dankmemer.services/api/trigger?avatar1={user.avatar_url}', headers=headers) as r:
                resp = await r.content.read()
                b = io.BytesIO(resp)
                f = discord.File(b, filename="triggered.gif")
                await ctx.send(file=f)

    @commands.command(aliases = ["merica"])
    async def america(self, ctx, user: discord.Member = None):
        check = await self.bot.pool.fetchval("SELECT level FROM donator WHERE userid = $1", ctx.author.id)
        if not check:
            em = discord.Embed(color=discord.Color.dark_teal())
            em.add_field(name="Donator Command", value=f"This is a patreon only command. To become a supporter, go [here](https://patreon.com/pdpbot).")
            await ctx.send(embed=em)
            return
            
        if user == None:
            user = ctx.author

        dmapikey = await self.bot.pool.fetchval("SELECT key FROM apikeys WHERE name = $1", "dankmemer")
        if dmapikey == None:
            await ctx.send("The Dank Memer API key has not been set.")
            return

        await ctx.channel.trigger_typing()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": dmapikey
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://dankmemer.services/api/america?avatar1={user.avatar_url}', headers=headers) as r:
                resp = await r.content.read()
                b = io.BytesIO(resp)
                f = discord.File(b, filename="america.gif")
                await ctx.send(file=f)

    @commands.command()
    async def salty(self, ctx, user: discord.Member = None):
        check = await self.bot.pool.fetchval("SELECT level FROM donator WHERE userid = $1", ctx.author.id)
        if not check:
            em = discord.Embed(color=discord.Color.dark_teal())
            em.add_field(name="Donator Command", value=f"This is a patreon only command. To become a supporter, go [here](https://patreon.com/pdpbot).")
            await ctx.send(embed=em)
            return
            
        if user == None:
            user = ctx.author

        dmapikey = await self.bot.pool.fetchval("SELECT key FROM apikeys WHERE name = $1", "dankmemer")
        if dmapikey == None:
            await ctx.send("The Dank Memer API key has not been set.")
            return

        await ctx.channel.trigger_typing()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": dmapikey
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://dankmemer.services/api/salty?avatar1={user.avatar_url}', headers=headers) as r:
                resp = await r.content.read()
                b = io.BytesIO(resp)
                f = discord.File(b, filename="salty.gif")
                await ctx.send(file=f)

    @commands.command()
    async def wanted(self, ctx, user: discord.Member = None):
        check = await self.bot.pool.fetchval("SELECT level FROM donator WHERE userid = $1", ctx.author.id)
        if not check:
            em = discord.Embed(color=discord.Color.dark_teal())
            em.add_field(name="Donator Command", value=f"This is a patreon only command. To become a supporter, go [here](https://patreon.com/pdpbot).")
            await ctx.send(embed=em)
            return
            
        if user == None:
            user = ctx.author

        dmapikey = await self.bot.pool.fetchval("SELECT key FROM apikeys WHERE name = $1", "dankmemer")
        if dmapikey == None:
            await ctx.send("The Dank Memer API key has not been set.")
            return

        await ctx.channel.trigger_typing()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": dmapikey
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://dankmemer.services/api/wanted?avatar1={user.avatar_url}', headers=headers) as r:
                resp = await r.content.read()
                b = io.BytesIO(resp)
                f = discord.File(b, filename="wanted.png")
                await ctx.send(file=f)

    @commands.command()
    async def gay(self, ctx, user: discord.Member = None):
        check = await self.bot.pool.fetchval("SELECT level FROM donator WHERE userid = $1", ctx.author.id)
        if not check:
            em = discord.Embed(color=discord.Color.dark_teal())
            em.add_field(name="Donator Command", value=f"This is a patreon only command. To become a supporter, go [here](https://patreon.com/pdpbot).")
            await ctx.send(embed=em)
            return
            
        if user == None:
            user = ctx.author

        dmapikey = await self.bot.pool.fetchval("SELECT key FROM apikeys WHERE name = $1", "dankmemer")
        if dmapikey == None:
            await ctx.send("The Dank Memer API key has not been set.")
            return

        await ctx.channel.trigger_typing()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": dmapikey
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://dankmemer.services/api/gay?avatar1={user.avatar_url}', headers=headers) as r:
                resp = await r.content.read()
                b = io.BytesIO(resp)
                f = discord.File(b, filename="gay.png")
                await ctx.send(file=f)


def setup(bot):
    bot.add_cog(Image(bot))