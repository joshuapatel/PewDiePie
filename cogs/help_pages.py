import discord
from discord.ext import commands


class HelpPages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def main(self, ctx):
        em = discord.Embed(color = discord.Color.gold())
        prefix = ctx.prefix.replace(self.bot.user.mention, f"@{self.bot.user.name}")
        em.set_author(name = "Main Commands")

        em.add_field(name = f"{prefix}disstrack [leave/stop]", value = "Plays Bitch Lasagna in a voice channel", inline = False)
        em.add_field(name = f"{prefix}congrats [leave/stop]", value = "Plays Congratulations in a voice channel", inline = False)
        em.add_field(name = f"{prefix}randomvid", value = "Returns a random PewDiePie or T-Series video", inline = False)
        em.add_field(name = f"{prefix}youtube (yt)", value = "Sends you the link to PewDiePie's and T-Series' YouTube channel", inline = False)
        em.add_field(name = f"{prefix}spoiler [message]", value = "Sends any message you provide as a spoiler in an annoying form", inline = False)
        em.add_field(name = f"{prefix}meme", value = "Sends a random meme from one of the best meme subreddits", inline = False)
        em.add_field(name = f"{prefix}joke", value = "Sends a random joke", inline = False)
        em.add_field(name = f"{prefix}dadjoke", value = "Sends a random dad joke", inline = False)
        em.add_field(name = f"{prefix}userinfo [@user]", value = "Gives you info about the specified user.", inline = False)
        em.add_field(name = f"{prefix}challenge [easy/medium/hard]", value = "Gives you a random challenge to complete", inline = False)
        em.add_field(name = f"{prefix}social", value = "Shows PewDiePie's social media links", inline = False)

        return em

    async def normal(self, ctx):
        em = discord.Embed(color = discord.Color.gold())
        prefix = ctx.prefix.replace(self.bot.user.mention, f"@{self.bot.user.name}")
        em.set_author(name = "Meta Commands")

        em.add_field(name = f"{prefix}info (about)", value = "Bot information", inline = False)
        em.add_field(name = f"{prefix}invite", value = "Sends the bot invite", inline = False)
        em.add_field(name = f"{prefix}feedback [message]", value = """
        This command will send the developer feedback on this bot. Feel free to send suggestions or issues
        """, inline = False)
        em.add_field(name = f"{prefix}prefixtut", value = f"This will give you a tutorial on how to use custom prefixes on {self.bot.user.name}", inline = False)
        em.add_field(name = f"{prefix}prefix", value = f"Returns the current prefix that {self.bot.user.name} uses in your server", inline = False)
        em.add_field(name = f"{prefix}setprefix (sprefix) [prefix]", value = "Sets the bot prefix or resets it if there is no prefix defined", inline = False)

        return em

    async def economy(self, ctx):
        em = discord.Embed(color = discord.Color.gold())
        prefix = ctx.prefix.replace(self.bot.user.mention, f"@{self.bot.user.name}")
        em.set_author(name = "Economy Commands")

        em.add_field(name = f"{prefix}shovel", value = "You work all day shoveling for Bro Coins", inline = False)
        em.add_field(name = f"{prefix}daily", value = "You get a bonus for shoveling", inline = False)
        em.add_field(name = f"{prefix}crime", value = "You commit a crime and gain or lose coins based on your success", inline = False)
        em.add_field(name = f"{prefix}balance (bal) [optional: user]", value = "Shows a users Bro Coin balance", inline = False)
        em.add_field(name = f"{prefix}pay", value = "Pays a user with a specified amount of Bro Coins", inline = False)
        em.add_field(name = f"{prefix}leaderboard (lb)", value = "Shows the leaderboard for Bro Coins", inline = False)
        em.add_field(name = f"{prefix}leaderboard server (guild)", value = "Shows the leaderboard of Bro Coins for your server", inline = False)
        em.add_field(name = f"{prefix}gamble [coins/all]", value = "You can gamble a specific amount of Bro Coins", inline = False)
        em.add_field(name = f"{prefix}steal (rob) [@user (or name)]", value = "Steals from a user that you specify", inline = False)
        em.add_field(name = f"{prefix}transfer [coins/all] [server name]", value = """
        Sends Bro Coins to another server. The max amount is 50% of your coins.
        """, inline = False)
        em.add_field(name = f"{prefix}statistics (stats)", value = "Statistics on Bro Coin usage", inline = False)

        return em

    async def shop(self, ctx):
        em = discord.Embed(color = discord.Color.gold())
        prefix = ctx.prefix.replace(self.bot.user.mention, f"@{self.bot.user.name}")
        em.set_author(name = "Economy Shop Commands")

        em.add_field(name = f"{prefix}shop", value = "View all the items (roles) in the shop", inline = False)
        em.add_field(name = f"{prefix}shop add [amount] [role name]", value = "Adds a role to the shop", inline = False)
        em.add_field(name = f"{prefix}shop edit [amount] [role name]", value = "Edits a roles cost in the shop", inline = False)
        em.add_field(name = f"{prefix}shop delete (remove) [role name]", value = "Removes a role from the shop", inline = False)
        em.add_field(name = f"{prefix}shop buy [role name]", value = "Buys an item from the shop", inline = False)
        em.set_footer(text = "Note: The bot must have the manage roles permission and be higher than the role in the shop to use the shop features")

        return em

    async def snipe(self, ctx):
        em = discord.Embed(color = discord.Color.gold())
        prefix = ctx.prefix.replace(self.bot.user.mention, f"@{self.bot.user.name}")
        em.set_author(name = "Snipe Commands")

        em.add_field(name = f"{prefix}snipe", value = "Shows the last deleted message in the current channel", inline = False)
        em.add_field(name = f"{prefix}snipe channel (ch) [channel]", value = "Snipes the last deleted message in the channel provided", inline = False)
        em.add_field(name = f"{prefix}snipe member (u) [@user (or name)]", value = """
        Snipes the last deleted message from the user provided in the current channel
        """, inline = False)
        em.add_field(name = f"{prefix}snipe count (c) [count]", value = """
        Snipes the [count] message in the current channel
        """, inline = False)
        em.add_field(name = f"{prefix}snipe list (l)", value = """
        List the previous 5 deleted messages in the server
        """, inline = False)
        em.add_field(name = f"{prefix}snipe bot (b)", value = """
        Snipes the last deleted message sent by a bot in the current channel
        """, inline = False)
        em.set_footer(text = "If you would like a snipe removed, please DM me with the message ID")

        return em

    async def moderation(self, ctx):
        em = discord.Embed(color = discord.Color.gold())
        prefix = ctx.prefix.replace(self.bot.user.mention, f"@{self.bot.user.name}")
        em.set_author(name = "Moderation Commands")

        em.add_field(name = f"{prefix}ban [@user] [optional: reason]", value = "Bans a member",
        inline = False)
        em.add_field(name = f"{prefix}kick [@user] [optional: reason]", value = "Kicks a member",
        inline = False)
        em.add_field(name = f"{prefix}purge [amount of messages]", value = "Purges a specified amount of messages from the channel",
        inline = False)
        em.add_field(name = f"{prefix}deafen [@user]", value = "Deafens a user. They must be in a voice channel",
        inline = False)
        em.add_field(name = f"{prefix}undeafen [@user]", value = "Undeafens a user. They must be in a voice channel",
        inline = False)
        em.add_field(name = f"{prefix}setnick [@user] [nickname]", value = "Sets a user's nickname. If there is none provided, it will reset it",
        inline = False)
        em.add_field(name = f"{prefix}warn [@user] [reason]", value = "Warns a user", inline = False)
        em.add_field(name = f"{prefix}warns [optional: @user]", value = "Gets a list of a users warnings. If none is provided, it'll show warnings in the server", inline = False)

        return em

    async def patreon(self, ctx):
        em = discord.Embed(color = discord.Color.gold())
        prefix = ctx.prefix.replace(self.bot.user.mention, f"@{self.bot.user.name}")
        em.set_author(name = "Patreon Commands")
        
        em.add_field(name = f"{prefix}america [@user]", value = "MURRRRICA!", inline = False)
        em.add_field(name = f"{prefix}changemymind [text]", value = "PewDiePie is awesome, change my mind.", inline = False)
        em.add_field(name = f"{prefix}salty [@user]", value = "SALTYYYY", inline = False)
        em.add_field(name = f"{prefix}triggered [@user]", value = "U mad bro?", inline = False)
        em.add_field(name = f"{prefix}trumptweet [text]", value = "~~#Trump2020~~", inline = False)
        em.add_field(name = f"{prefix}wanted [@user]", value = "This down aint' big enough for the two of us 🔫", inline = False)
        em.add_field(name = f"{prefix}weekly", value = "Cash's in your weekly check", inline = False)
        em.set_footer(text = "To become a supporter, go https://patreon.com/pdpbot")

        return em


def setup(bot):
    bot.add_cog(HelpPages(bot))