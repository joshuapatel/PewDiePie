"""
Rename this file to config.py. You will need PostgreSQL, discord.py rewrite, asyncpg, and jishaku.

Download PostgreSQL: https://www.postgresql.org/download/

discord.py rewrite: `pip install -U discord.py[voice]`

asyncpg: `pip install -U asyncpg`

jishaku: `pip install -U jishaku`
"""

privtoken = "" # Use this token for testing on your development bot
pubtoken = "" # Use this token on your live bot

# The bot will automatically start with the pubtoken token.
# You can search for "config.pubtoken" in the pewdiepie.py file and change that

dbltoken = "" # This is your Discord Bot List token. If you don't have one, change "" to None

ytdapi = "" # This is your token for accessing YouTube's API. You MUST have this to use the subcount command

db_user = "" # Username for logging into your database
db_password = "" # Password for your database

# Please note that you must have a database called tseries