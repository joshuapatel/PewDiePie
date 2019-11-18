import discord
from discord.ext import commands
from jishaku import help_command


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = help_command.MinimalEmbedPaginatorHelp()

    def cog_unload(self):
        self.bot.help_command = None


def setup(bot):
    bot.add_cog(Help(bot))
