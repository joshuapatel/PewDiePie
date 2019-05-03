# -> Discord
import discord
from discord.ext import commands
# -> Configuration
import config
# -> Miscellaneous
import random
import datetime
# -> Database and cache
import asyncpg
import aioredis
# -> Loop
import asyncio
import sys
import os

# Supports asyncio subprocesses for Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

async def custom_prefix(bot, message):
    await bot.wait_until_ready()

    try:
        prefix = bot.prefixes.get(message.guild.id)
    except AttributeError:
        rnd = random.randint(12**2, 12**4)
        return str(rnd)

    if prefix == None:
        return commands.when_mentioned_or(*bot.default_prefixes)(bot, message)
    else:
        return commands.when_mentioned_or(prefix)(bot, message)

extensions = ["jishaku", "cogs.functions"]

for f in os.listdir("cogs"):
    if f.endswith(".py") and not f"cogs.{f[:-3]}" in extensions:
        extensions.append("cogs." + f[:-3])

class PewDiePie(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix = custom_prefix,
            case_insensitive = True,
            max_messages = 500,
            fetch_offline_members = False,
            reconnect = True,
            owner_id = 498678645716418578
        )
        self.prefixes = {}
        self.pool = None
        self.redis = None

    async def on_ready(self):
        if not hasattr(self, "uptime"):
            self.uptime = datetime.datetime.utcnow()

        print(f"{self.user.name} is ready!")

    async def on_connect(self):
        pool_creds = {
            "user": config.db_user,
            "password": config.db_password,
            "port": 5432,
            "host": "localhost",
            "database": "tseries"
        }

        redis_creds = {
            "address": ("localhost", 6379)
        }

        try:
            self.pool = await asyncpg.create_pool(**pool_creds)
            self.redis = await aioredis.create_redis_pool(**redis_creds)
        except Exception as e:
            print("There was a problem")
            print("\n" + str(e))

        with open("schema.sql", "r") as schema:
            await self.pool.execute(schema.read())

        self.default_prefixes = [
            "p.", "P.", "p!", "P!",
            "t.", "t!", "ts!", "ts.",
            "Ts!", "tS!", "TS!", "T.", "T!",
            "Ts.", "tS.", "TS."
        ]

        for extension in extensions:
            try:
                self.load_extension(extension)
            except Exception as error:
                print(f"There was a problem loading in the {extension} extension")
                print(f"\n{error}")

    async def start(self):
        await self.login(config.pubtoken) # pylint: disable=no-member
        try:
            await self.connect()
        except KeyboardInterrupt:
            await self.stop()

    async def stop(self):
        await self.pool.close()
        await super().logout()

    def run(self):
        loop = self.loop
        try:
            loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            loop.run_until_complete(self.stop())


if __name__ == "__main__":
    PewDiePie().run()