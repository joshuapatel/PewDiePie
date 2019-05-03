import discord
from discord.ext import commands
import utils.paginator as paginator


class Paginator(paginator.EmbedInterface):
    def __init__(self, ctx, pag):
        self.ctx = ctx
        self.p = pag
        super().__init__(self.ctx.bot, self.p, self.ctx.author)

    async def send_pages(self):
        await self.send_to(self.ctx)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_pages = bot.get_cog("HelpPages")
        self.bot.remove_command("help")

    @commands.command()
    async def help(self, ctx):
        pag = paginator.EmbedPaginator()

        hp = ("main", "normal", "economy", "shop", "snipe", "moderation")

        for p in hp:
            pag.add_page(await getattr(self.help_pages, p)(ctx))

        interface = Paginator(ctx, pag)
        await interface.send_pages()


def setup(bot):
    bot.add_cog(Help(bot))