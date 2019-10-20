# PewDiePie Discord Bot

Do you have any more questions about the bot? Send a DM to **Kowlin#4417 or A Trash Coder#0981** or join the [support server](https://discord.gg/we4DQ5u).

## Why did I make this bot?

I made this bot because I was very intrigued into the PewDiePie vs T-Series war. I wanted to do my part and make a bot.

## How do I get authorized for the subgap command?

You do not need to get authorized for this command anymore. Simply run `p.subgap` in your subgap channel and it should work. You can change the channels being compared by running `p.setup`.

## How should I run the bot?

I strongly recommend that you [invite the bot](https://discordapp.com/oauth2/authorize?client_id=500868806776979462&scope=bot&permissions=338717761). Nevertheless, here are the instructions.

### Instructions

1. **Install Python 3.6+**

I use Python 3.7 for production and testing purposes so results may vary.

2. **Install dependencies**

Run `pip install -U -r requirements.txt`

3. **Install PostgreSQL**

The latest version of PostgreSQL is recommended.

You will need...

+ A database named `tseries`
+ Username and password

Note your username and password.

4. **Fill out credentials**

Open up `config-example.py` and follow the instructions in the docstring.

5. **Start the bot**

Run `python pewdiepie.py`

## Commands

### General Commands
|Name|Description|
|----|-----------|
|challenge|Sends a challenge to complete|
|disstrack|Plays Bitch Lasagna in a voice channel|
|disstrack stop (leave)|Disconnects from the voice channel|
|congrats|Plays Congratulations in a voice channel|
|congrats stop (leave)|Disconnects from the voice channel|
|8ball [question]|Ask the bot a question|
|dadjoke|Sends a really funny joke|
|endpoll [id]|Ends the specified poll|
|joke|Sends a funny joke|
|meme|Gets and sends a beautiful meme picked straight from Reddit|
|poll [message]|Starts a poll|
|randomvid|Returns a random PewDiePie or T-Series video|
|serverinfo|Sends information on the server|
|social|Sends PewDiePie's socials|
|spoiler|Sends any message you provide as a spoiler in an annoying form|
|userinfo [optional: user]|Sends information on a specified user|
|weather [location]|Sends weather on a location|
|youtube (yt)|Sends you the link to PewDiePie's and T-Series' YouTube channel|

### Bro Coin Commands (economy)
|Name|Description|
|----|-----------|
|ask|Ask a celeberty for money|
|balance (bal)|Informs you on the amount of Bro Coins you have|
|crime|You commit a crime and gain or lose coins based on your success|
|daily|Reedems your daily bonus of Bro Coins|
|gamble|Gambles all or a specific amount of Bro Coins|
|leaderboard (lb)|Shows the leaderboard for Bro Coins|
|leaderboard server (guild)|Shows the leaderboard of Bro Coins for your server|
|pay|Pays another user a specified amount of Bro Coins|
|shovel|You work all day by shoveling for Bro Coins|
|statistics (stats)|Statistics on Bro Coin usage|
|steal (rob)|Steals from a user|
|transfer|Sends any amount that you specify to another server. The max amount is 50% of your coins|
|phrase [id]|Retrieves a phrase|

### Shop Commands for Bro Coin
|Name|Description|
|----|-----------|
|shop|View all items (roles) in the shop|
|shop add|Adds a role to the shop (you must have the manage roles permission)|
|shop edit|Edits a role (eg. changes the cost) in the shop (manage roles permission required by user)|
|shop delete (remove)|Removes a role from the shop (manage roles permission required by user)|
|shop buy|Buys an item from the shop (you must have enough coins)|

### Snipe Commands
|Name|Description|
|---|------------|
|snipe|Shows the last deleted message in the current channel|
|snipe channel (ch)|Snipes the last deleted message in the channel provided|
|snipe member (u)|Snipes the last deleted message from the user provided in the current channel|
|snipe count (c)|Snipes the [count] message in the current channel|
|snipe list (l)|List the previous 5 deleted messages in the server|
|snipe bot (b)|Snipes the last deleted message sent by a bot in the current channel|

### Moderation Commands
|Name|Description|
|----|-----------|
|ban|Bans a member. Reason is optional|
|deafen|Deafens a user. They must be in a voice channel|
|kick|Kicks a member. Reason is optional|
|purge|Purges / clears a specified amount of messages|
|setnick|Sets a user's nickname. If none is provided, it will be reset|
|undeafen|Undeafens a user. They must be in a voice channel|
|warn|Warns a user|
|warns|Retrieves warnings for the user specified|

### Other Commands
|Name|Description|
|----|-----------|
|botinfo|Information on the bot|
|invite|Sends the bot invite|
|feedback|This command will send the developer feedback on this bot. Feel free to send suggestions or issues|
|prefixtut|This will give you a tutorial on how to use custom prefixes on the bot|
|prefix|Returns the current prefix which the bot uses in your server|
|setprefix (sprefix)|Sets the bot prefix or resets it if there is no prefix defined|

[![Discord Bots](https://discordbots.org/api/widget/500868806776979462.svg)](https://discordbots.org/bot/500868806776979462)
