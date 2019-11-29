# -> Discord
import discord
from discord.ext import commands, tasks
# -> Miscellaneous
import datetime
# -> Loop
import aiohttp
import asyncio
# -> Configuration
import sys
sys.path.append("../")
import config


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.JOIN_LEAVE_LOG = 501089724421767178
        self.autostatus.start()

    def cog_unload(self):
        self.autostatus.cancel()

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        prefix = self.bot.prefixes.get(ctx.guild.id, None) or "p."
        print()
        print(f"COMPLETED COMMAND: {ctx.command.name}. Invoked by: {ctx.author.name}#{ctx.author.discriminator}")
        print(f"GUILD: {ctx.guild.name} | GUILD ID: {ctx.guild.id}\nUSER ID: {ctx.author.id} | CHANNEL ID: {ctx.channel.id}")
        await ctx.send(f"The bot is going away. Read more in the announcements channel in the Discord server (run `{prefix}info` to get the invite).")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined guild named '{guild.name}' with {guild.member_count} members")

        logchannel = self.bot.get_channel(self.JOIN_LEAVE_LOG)
        em = discord.Embed(title = "Joined Guild", color = discord.Color.teal())
        bot_count = len([b for b in guild.members if b.bot])
        em.set_thumbnail(url = guild.icon_url)
        em.add_field(name = "Name", value = guild.name)
        em.add_field(name = "ID", value = str(guild.id))
        em.add_field(name = "Owner", value = str(guild.owner))
        em.add_field(name = "Member Count", value = f"{guild.member_count:,d}")
        em.add_field(name = "Bot Count", value = format(bot_count, ",d"))
        em.add_field(name = "Human Count", value = format(guild.member_count - bot_count, ",d"))
        em.add_field(name = "Verification Level", value = str(guild.verification_level))
        em.add_field(name = "Channel Count", value = f"{len(guild.channels):,d}")
        em.add_field(name = "Creation Time", value = guild.created_at)

        em.timestamp = datetime.datetime.utcnow()
        await logchannel.send(embed = em)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print(f"Left guild named '{guild.name}' that had {guild.member_count} members")

        logchannel = self.bot.get_channel(self.JOIN_LEAVE_LOG)
        em = discord.Embed(title = "Left Guild", color = discord.Color.purple())
        bot_count = len([b for b in guild.members if b.bot])
        em.set_thumbnail(url = guild.icon_url)
        em.add_field(name = "Name", value = guild.name)
        em.add_field(name = "ID", value = str(guild.id))
        em.add_field(name = "Owner", value = str(guild.owner))
        em.add_field(name = "Member Count", value = f"{guild.member_count:,d}")
        em.add_field(name = "Bot Count", value = format(bot_count, ",d"))
        em.add_field(name = "Human Count", value = format(guild.member_count - bot_count, ",d"))
        em.add_field(name = "Verification Level", value = str(guild.verification_level))
        em.add_field(name = "Channel Count", value = f"{len(guild.channels):,d}")
        em.add_field(name = "Creation Time", value = guild.created_at)

        em.timestamp = datetime.datetime.utcnow()
        await logchannel.send(embed = em)

    @tasks.loop(seconds = 30)
    async def autostatus(self):
        watching = "The bot is going away"

        await self.bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = watching))

    @autostatus.before_loop
    async def before_autostatus(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Events(bot))