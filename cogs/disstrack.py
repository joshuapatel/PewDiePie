import discord
from discord.ext import commands


class Disstrack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def play_song(self, ctx, name: str = "lasagna.mp3"):
        if ctx.author.voice != None:
            try:
                await ctx.author.voice.channel.connect()
            except discord.ClientException:
                pass

            source = discord.FFmpegPCMAudio(name)

            try:
                ctx.voice_client.play(source)
            except discord.ClientException:
                await ctx.send("Already playing audio")
                return
            await ctx.send(f"Connected to `{ctx.voice_client.channel.name}`")
        else:
            await ctx.send("You must be connected to a voice channel")

    async def stop(self, ctx):
        if ctx.voice_client != None:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected from voice channel")
        else:
            await ctx.send(f"{self.bot.user.name} is not currently in a voice channel")

    @commands.group(invoke_without_command = True)
    async def congrats(self, ctx):
        await self.play_song(ctx, "congrats.mp3")

    @congrats.command(name = "stop", aliases = ["leave", "end", "disconnect"])
    async def congrats_stop(self, ctx):
        await self.stop(ctx)

    @commands.group(invoke_without_command = True)
    async def disstrack(self, ctx):
        await self.play_song(ctx)

    @disstrack.command(name = "stop", aliases = ["leave", "end", "disconnect"])
    async def disstrack_stop(self, ctx):
        await self.stop(ctx)

def setup(bot):
    bot.add_cog(Disstrack(bot))