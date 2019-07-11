# -> Discord
import discord
from discord.ext import commands

import aiohttp

import struct
import io
import contextlib
import utils.BytesIO


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
        if user == None:
            user = ctx.author

        dmapikey = await self.bot.pool.fetchval("SELECT dankmemer FROM apikeys")
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
                await ctx.send(f"`{resp}`")


def setup(bot):
    bot.add_cog(Image(bot))