# -> Discord
import discord
from discord.ext import commands
# -> Miscellaneous
import re
import inspect
import utils.paginator as paginator
# -> Loop
import asyncio

class Paginator(paginator.EmbedInterface):
    def __init__(self, ctx, pag):
        self.ctx = ctx
        self.p = pag
        super().__init__(self.ctx.bot, self.p, self.ctx.author)

    async def send_pages(self):
        await self.send_to(self.ctx)

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

    @commands.group(invoke_without_command=True)
    async def fbblacklist(self, ctx):
        await ctx.send("**Options:** add, remove")

    @fbblacklist.command()
    async def add(self, ctx, *, user: discord.Member):
        fbcheck = await self.bot.pool.fetchrow("SELECT * FROM fbblocked WHERE userid = $1", user.id)
        if fbcheck != None:
            return await ctx.send("This user is already blacklisted from the feedback command.")
        
        await self.bot.pool.execute("INSERT INTO fbblocked VALUES ($1)", user.id)
        em = discord.Embed(title = "Blacklisted", description = "This user has been blacklisted from using the feedback command.", color = discord.Color.red())
        await ctx.send(embed = em)

    @fbblacklist.command()
    async def remove(self, ctx, *, user: discord.Member):
        fbcheck = await self.bot.pool.fetchrow("SELECT * FROM fbblocked WHERE userid = $1", user.id)
        if fbcheck == None:
            return await ctx.send("This user is not blacklisted from the feedback command.")
        
        await self.bot.pool.execute("DELETE FROM fbblocked WHERE userid = $1", user.id)
        em = discord.Embed(title = "Un-Blacklisted", description = "This user has been un-blacklisted from using the feedback command.", color = discord.Color.red())
        await ctx.send(embed = em)

    @commands.group(invoke_without_command=True)
    async def blacklist(self, ctx):
        await ctx.send("**Options:** add, remove")

    @blacklist.command()
    async def add(self, ctx, *, user: discord.Member):
        bcheck = await self.bot.pool.fetchrow("SELECT * FROM blacklist WHERE userid = $1", user.id)
        if bcheck != None:
            return await ctx.send("This user is already blacklisted from the feedback command.")

        await self.bot.pool.execute("INSERT INTO blacklist VALUES ($1)", user.id)
        em = discord.Embed(title = "Blacklisted", description = "This user has been blacklisted from using commands.", color = discord.Color.red())
        await ctx.send(embed = em)

    @blacklist.command()
    async def remove(self, ctx, *, user: discord.Member):
        bcheck = await self.bot.pool.fetchrow("SELECT * FROM blacklist WHERE userid = $1", user.id)
        if bcheck == None:
            return await ctx.send("This user is not blacklisted from using commands.")
        
        await self.bot.pool.execute("DELETE FROM blacklist WHERE userid = $1", user.id)
        em = discord.Embed(title = "Un-Blacklisted", description = "This user has been un-blacklisted from using commands.", color = discord.Color.red())
        await ctx.send(embed = em)

    @commands.command()
    async def echo(self, ctx, *, message: str):
        await ctx.send(message)
        await ctx.message.delete()

    @commands.command()
    async def delsnipe(self, ctx, *, contents: str):
        check = await self.bot.pool.fetch("SELECT * FROM snipe WHERE guild = $1 AND contents = $2", ctx.guild.id, contents)
        if check == None:
            await ctx.send("That deleted message is not in the snipe database.")
            return

        try:
            await self.bot.pool.execute("DELETE FROM snipe WHERE guild = $1 AND contents = $2", ctx.guild.id, contents)
            await ctx.send("I have deleted that message from the snipe database.")
        except:
            await ctx.send("An error occurred while deleting that message from the snipe database.")

    @commands.group(invoke_without_command = True)
    async def setkey(self, ctx):
        await ctx.send("**Options:** dankmemer")

    @setkey.command()
    async def dankmemer(self, ctx, *, key: str):
        await self.bot.pool.execute("UPDATE apikeys SET dankmemer = $1", key)
        await ctx.send("Successfully updated the Dank Memer API key!")

    @commands.group(invoke_without_command = True)
    @commands.is_owner()
    async def patreon(self, ctx):
        embed = discord.Embed(title = "Available Patreon Commands:", color = discord.Color.dark_teal(), description = "``p.patreon add [donator lvl] [user]`` \n\n ``p.patreon remove [user]``")
        await ctx.send(embed = embed)

    @patreon.command()
    @commands.is_owner()
    async def add(self, ctx, lvl:int, *, user: discord.Member):
        if lvl > 3:
            await ctx.send(f"There is no lvl {lvl} supporter.")
            return

        check = await self.bot.pool.fetch("SELECT * FROM donator WHERE userid = $1", user.id)
        if check:
            embed = discord.Embed(title = "Negative!", color = discord.Color.red(), description = f"{user.name} is already a patreon.")
            await ctx.send(embed = embed)
            return
        
        await self.bot.pool.execute("INSERT INTO donator VALUES ($1, $2)", user.id, lvl)
        embed = discord.Embed(title = "Done!", color = discord.Color.dark_teal(), description = f"Added {user.name} as a patreon.")
        await ctx.send(embed = embed)

    @patreon.command()
    @commands.is_owner()
    async def remove(self, ctx, *, user: discord.Member):
        check = await self.bot.pool.fetch("SELECT * FROM donator WHERE userid = $1", user.id)
        if not check:
            embed = discord.Embed(title = "Negative!", color = discord.Color.red(), description = f"{user.name} is not a patreon.")
            await ctx.send(embed = embed)   
            return         
   
        await self.bot.pool.execute("DELETE FROM donator WHERE userid = $1", user.id)
        embed = discord.Embed(title = "Done!", color = discord.Color.dark_teal(), description = f"Removed {user.name} as a patreon.")
        await ctx.send(embed = embed)

    @commands.group(invoke_without_command = True)
    @commands.is_owner()
    async def keys(self, ctx):
        keys = await self.bot.pool.fetch("SELECT * FROM apikeys")

        if keys == []:
            em = discord.Embed(color = discord.Color.red())
            em.add_field(name = "No API Keys", value = "No API Keys have been found.")
            await ctx.send(embed = em)
            return

        pag = paginator.EmbedPaginator()

        for key in keys:
            em = discord.Embed(titile = "API Keys", color = discord.Color.red())
            em.add_field(name = "Name:", value = key['key'])
            em.add_field(name = "Key:", value = key['key'])


            pag.add_page(em)

        interface = Paginator(ctx, pag)
        await interface.send_pages()

    @keys.command()
    @commands.is_owner()
    async def add(self, ctx, key, *, name):
        check = await self.bot.pool.fetch("SELECT * FROM apikeys WHERE name = $1", name)
        if check:
            em = discord.Embed(color = discord.Color.red())
            em.add_field(name = "Error", value = "That is already a name in the DB.")
            await ctx.send(embed = em)
            return

        await self.bot.pool.execute("INSERT INTO apikeys VALUES ($1. $2)", name, key)

        embed = discord.Embed(title = "Done!", color = discord.Colour.dark_teal(), description = f"{name} has been added as a key")
        await ctx.send(embed = embed)



def setup(bot):
    bot.add_cog(Owner(bot))