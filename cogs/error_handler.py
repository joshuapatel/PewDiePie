import discord
from discord.ext import commands
import humanize


class ErrorHandler(commands.Cog, name="Error Handler"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if not isinstance(error, commands.CommandOnCooldown):
            try:
                self.bot.get_command(ctx.command.name).reset_cooldown(ctx)
            except AttributeError:
                pass

        errors = {
            commands.MissingPermissions: {"msg": "You are missing permissions to run this command.", "ty": "Missing Permissions"},
            commands.BotMissingPermissions: {"msg": "The bot does not have permissions to run this command.", "ty": "Bot Missing Permissions"},
            discord.HTTPException: {"msg": "There was an error connecting to Discord. Please try again.", "ty": "HTTP Exception"},
            commands.CommandInvokeError: {"msg": "There was an issue running the command.\n[ERROR]", "ty": "Command Invoke Error"},
            commands.NotOwner: {"msg": "You are not an owner.", "ty": "Not Owner"}
        }

        ex = (commands.MissingRequiredArgument, commands.CommandOnCooldown, commands.CommandNotFound)

        if not isinstance(error, ex):
            ets = errors.get(error.__class__)
            if ets == None:
                ets = {}
                ets["msg"] = "An unexpected error has occurred.\n[ERROR]"
                ets["ty"] = "Unexpected Error"

            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = f"Error: {ets['ty']}", value = ets["msg"].replace("[ERROR]", f"```\n{error}\n```"))

            try:
                await ctx.send(embed = em)
            except discord.Forbidden:
                try:
                    await ctx.author.send(embed = em)
                except:
                    pass

        if isinstance(error, commands.CheckFailure):
            return

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Error: Missing Argument", value = f"""
            I'm missing a parameter, `{str(error.param).partition(':')[0]}`.
            Make sure you ran the command correctly then try again.
            """)
            await ctx.send(embed = em)

        elif isinstance(error, commands.CommandOnCooldown):
            time = humanize.naturaldelta(error.retry_after)

            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Error: Cooldown", value = f"Please wait {time} to use `{ctx.command.name}` again")
            await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))