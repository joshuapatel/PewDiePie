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
        return str(random.random())

    if prefix is None:
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
            reconnect = True
        )
        self.pool = None
        self.prefixes = {}
        self.owner_role = config.owner
        self.owners = []

    async def on_ready(self):
        if not hasattr(self, "uptime"):
            self.uptime = datetime.datetime.utcnow()

        print(f"{self.user.name} is ready!")

    async def is_owner(self, user):
        return user.id in self.owners

    async def on_connect(self):
        # Database and cache
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
            await self.redis.flushdb(async_op = True)
        except Exception as error:
            print("There was a problem")
            print("\n" + str(error))
            await super().logout()

        with open("schema.sql", "r") as schema:
            await self.pool.execute(schema.read())

        # Owners
        if len(self.owner_role) == 2:
            guild = self.get_guild(self.owner_role[0])
            role = guild.get_role(self.owner_role[1])
            self.owners.extend([r.id for r in role.members])
        else:
            app = await self.application_info()
            self.owners.append(app.owner.id)

        # Prefixes
        self.default_prefixes = [
            "p.", "P.", "p!", "P!",
            "t.", "t!", "ts!", "ts.",
            "Ts!", "tS!", "TS!", "T.", "T!",
            "Ts.", "tS.", "TS."
        ]

        self.prefixes = dict(await self.pool.fetch("SELECT * FROM prefixes"))

        self.prepare_extensions()

    def prepare_extensions(self):
        for extension in extensions:
            try:
                self.load_extension(extension)
            except Exception as error:
                print(f"There was a problem loading in the {extension} extension")
                print("\n" + str(error))

    async def start(self):
        await self.login(config.pubtoken) # pylint: disable=no-member
        try:
            await self.connect()
        except KeyboardInterrupt:
            await self.stop()

    async def stop(self):
        self.redis.close()
        await self.redis.wait_closed()
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