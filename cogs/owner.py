# -> Discord
import discord
from discord.ext import commands
# -> Miscellaneous
import re
import inspect
# -> Loop
import asyncio


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not await self.bot.is_owner(ctx.author):
            raise commands.NotOwner()
        return True

    @commands.command()
    async def update(self, ctx):
        """Pulls the latest commit and updates cogs"""
        pro = await asyncio.create_subprocess_exec(
            "git", "pull",
            stdout = asyncio.subprocess.PIPE,
            stderr = asyncio.subprocess.PIPE
        )

        try:
            com = await asyncio.wait_for(pro.communicate(), timeout = 10)
            com = com[0].decode() + "\n" + com[1].decode()
        except asyncio.TimeoutError:
            await ctx.send("Took too long to respond")
            return

        reg = r"(.*?)\.py"
        found = re.findall(reg, com)

        if found:
            updated = []
            final_string = ""

            for x in found:
                extension = re.sub(r"\s+", "", x)
                extension = extension.replace("/", ".")

                try:
                    self.bot.reload_extension(extension)
                except ModuleNotFoundError:
                    continue
                except Exception as error:
                    if inspect.getfile(self.bot.__class__).replace(".py", "") in extension:
                        continue
                    else:
                        await ctx.send(f"Error: ```\n{error}\n```", delete_after = 5)
                        continue

                updated.append(extension)

            for b in updated:
                final_string += f"`{b}` "

            if updated == []:
                await ctx.send("No cogs were updated")
            else:
                await ctx.send(f"Updated cogs: {final_string}")
        else:
            await ctx.send("No cogs were updated")


def setup(bot):
    bot.add_cog(Owner(bot))