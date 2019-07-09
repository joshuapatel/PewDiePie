# -> Discord
import discord
from discord.ext import commands

import aiohttp


class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
                imgurl = raw['message']
                em = discord.Embed(title = "Change My Mind", color = discord.Color.red())
                em.set_image(url=imgurl)
                em.set_footer(text="NOTE: These commands are still in beta.")
                await ctx.send(embed = em)

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
                imgurl = raw['message']
                em = discord.Embed(title = "Trump Tweet", color = discord.Color.red())
                em.set_image(url=imgurl)
                em.set_footer(text="NOTE: These commands are still in beta.")
                await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Image(bot))