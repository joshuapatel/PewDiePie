import discord
from discord.ext import commands
import datetime
import cogs.utils.paginator as paginator


class Paginator(paginator.EmbedInterface):
    def __init__(self, ctx, pag):
        self.ctx = ctx
        self.p = pag
        super().__init__(self.ctx.bot, self.p, self.ctx.author)

    async def send_pages(self):
        await self.send_to(self.ctx)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def ban(self, ctx, user: discord.Member, *, reason: str = None):
        try:
            await user.ban(reason = reason)

            em = discord.Embed(color = discord.Color.red())
            em.add_field(name = "Banned", value = f"{user.mention} has been banned.")
            await ctx.send(embed = em)
        except discord.Forbidden:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Forbidden", value = "Please check that the bot has permissions to ban this member.")
            await ctx.send(embed = em)
            return

        try:
            if reason == None:
                r = "You have been banned."
            else:
                r = reason
            em = discord.Embed(color = discord.Color.red())
            em.add_field(name = f"Banned: {ctx.guild.name}", value = r)
            await user.send(embed = em)
        except discord.Forbidden:
            pass

    @commands.command()
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    async def kick(self, ctx, user: discord.Member, *, reason: str = None):
        try:
            await user.kick(reason = reason)

            em = discord.Embed(color = discord.Color.red())
            em.add_field(name = "Kicked", value = f"{user.mention} has been kicked.")
            await ctx.send(embed = em)
        except discord.Forbidden:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Forbidden", value = "Please check that the bot has permissions to kick this member.")
            await ctx.send(embed = em)
            return

        try:
            if reason == None:
                r = "You have been kicked."
            else:
                r = reason
            em = discord.Embed(color = discord.Color.red())
            em.add_field(name = f"Kicked: {ctx.guild.name}", value = r)
            await user.send(embed = em)
        except discord.Forbidden:
            pass

    @commands.command(aliases = ["delete", "remove"])
    @commands.has_permissions(manage_messages = True)
    @commands.bot_has_permissions(manage_messages = True)
    async def purge(self, ctx, amount: int = 5):
        try:
            await ctx.channel.purge(limit = amount + 1)
        except discord.Forbidden:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Forbidden", value = "Cannot purge messages. Please try again.")
            await ctx.send(embed = em)

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    @commands.bot_has_permissions(manage_guild = True)
    async def deafen(self, ctx, *, user: discord.Member):
        if user.voice == None:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Cannot Deafen", value = "You can only deafen members that are in a voice channel.")
            await ctx.send(embed = em)
            return

        await user.edit(deafen = True)

        em = discord.Embed(color = discord.Color.red())
        em.add_field(name = "Deafened Member", value = f"{user.mention} has been deafened.")
        await ctx.send(embed = em)

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    @commands.bot_has_permissions(manage_guild = True)
    async def undeafen(self, ctx, *, user: discord.Member):
        if user.voice == None:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Cannot Undeafen", value = "You can only undeafen members that are in a voice channel.")
            await ctx.send(embed = em)
            return

        await user.edit(deafen = False)

        em = discord.Embed(color = discord.Color.red())
        em.add_field(name = "Undeafened Member", value = f"{user.mention} has been undeafened.")
        await ctx.send(embed = em)

    @commands.command(aliases = ["setnick"])
    @commands.has_permissions(manage_nicknames = True)
    @commands.bot_has_permissions(manage_nicknames = True)
    async def setnickname(self, ctx, user: discord.Member, *, nickname: str = None):
        try:
            if nickname != None:
                await user.edit(nick = nickname[:32])
            else:
                await user.edit(nick = nickname)

            em = discord.Embed(color = discord.Color.red())

            if nickname == None:
                em.add_field(name = "Reset Nickname", value = f"{user.mention}'s nickname has been reset.")
            else:
                em.add_field(name = "Set Nickname", value = f"{user.mention}'s nickname has been set to `{nickname}`")

            await ctx.send(embed = em)
        except discord.Forbidden:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Forbidden", value = "Couldn't set users nickname. Check if the bot is higher than the user then try again.")
            await ctx.send(embed = em)

    @commands.command(aliases = ["warning"])
    @commands.has_permissions(kick_members = True)
    async def warn(self, ctx, user: discord.Member, *, reason: str = None):
        if reason == None:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Specify Reason", value = "You must include the reason.")
            await ctx.send(embed = em)
            return
        if user.id == ctx.author.id:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Cannot Warn Yourself", value = "You cannot warn yourself.")
            await ctx.send(embed = em)
            return

        await self.bot.pool.execute("INSERT INTO warns VALUES ($1, $2, $3, $4, $5, $6)",
        user.id, ctx.guild.id, ctx.author.id, ctx.author.name,
        reason, datetime.datetime.utcnow())

        em = discord.Embed(color = discord.Color.red())
        em.add_field(name = "Warned", value = f"{user.mention} has been warned.")
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = em)

        em = discord.Embed(color = discord.Color.red())
        em.add_field(name = f"Warned: {ctx.guild.name}", value = reason)
        em.timestamp = datetime.datetime.utcnow()
        try:
            await user.send(embed = em)
        except discord.Forbidden:
            pass

    @commands.command(aliases = ["warnings"])
    async def warns(self, ctx, *, user: discord.Member = None):
        if user == None:
            user = ctx.author

        warns = await self.bot.pool.fetch("SELECT * FROM warns WHERE userid = $1 AND guildid = $2", user.id, ctx.guild.id)

        if warns == []:
            em = discord.Embed(color = discord.Color.red())
            em.add_field(name = "No Warnings", value = f"{user.mention} has no warnings.")
            await ctx.send(embed = em)
            return

        pag = paginator.EmbedPaginator()

        for warning in warns:
            em = discord.Embed(color = discord.Color.red())
            em.description = f"{user.name} has {len(warns)} warning(s)."

            isname = ctx.guild.get_member(warning["issuerid"])

            if isname == None:
                isname = warning["issuername"]
            else:
                isname = isname.name

            em.add_field(name = f"Issued By: {isname}", value = warning["reason"])
            em.timestamp = warning["time"]

            pag.add_page(em)

        interface = Paginator(ctx, pag)
        await interface.send_pages()


def setup(bot):
    bot.add_cog(Moderation(bot))