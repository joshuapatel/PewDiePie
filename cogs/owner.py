# -> Discord
import discord
from discord.ext import commands
# -> Miscellaneous
import datetime
import re
import inspect
import psutil
# -> Eval
from contextlib import redirect_stdout
import textwrap
import io
import traceback
# -> Loop
import asyncio
# -> Configuration
import sys
sys.path.append("../")
import config # Note: Only importing config module since it's easier to use in eval


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not await self.bot.is_owner(ctx.author):
            raise commands.NotOwner()
        return True

    @commands.command()
    async def update(self, ctx):
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

    @commands.command()
    async def redis(self, ctx, *args):
        try:
            cmd = await self.bot.redis.execute(*args)
            await ctx.send(getattr(cmd, "decode", cmd.__str__)())
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(Owner(bot))