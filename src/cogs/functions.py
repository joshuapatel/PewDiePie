import discord
from discord.ext import commands


class Functions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def add(self):
        d = ["econ"]
        for entry in d:
            if not hasattr(self.bot, entry):
                setattr(self.bot, entry, {})

    @commands.Cog.listener()
    async def close(self):
        if hasattr(self.bot, "tasks"):
            for tsk in self.bot.tasks:
                tsk.cancel()


def setup(bot):
    bot.loop.create_task(Functions(bot).add())
    bot.add_cog(Functions(bot))