import asyncio
import logging
import logging.handlers
import os

from typing import List, Optional

import asyncpg  
import discord
from discord.ext import commands
from aiohttp import ClientSession

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

initial_extensions = [
    'cogs._commands'
]

class ReinBot(commands.Bot):
    def __init__(
        self,
        command_prefix: str,
        *args,
        db_pool: asyncpg.Pool,
        web_client: ClientSession,
        testing_guild_id: Optional[int] = None,
        intents: Optional[discord.Intents] = discord.Intents.all(),
        **kwargs,
    ):
        super().__init__(command_prefix=".", *args, intents=intents, **kwargs)
        self.db_pool = db_pool
        self.web_client = web_client
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions

    async def setup_hook(self) -> None:
        for extensions in initial_extensions:
            try: 
                await self.load_extension(extensions)
                print(f"{extensions} loaded!")
            except Exception as e:
                log.exception('Failed to load extension %s.', extension)
    
    async def on_ready(self) -> None:
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print('--------')

async def main():
    # Logger setup
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # start
    USER = config["POSTGRESQL"]["USER"]
    TOKEN = config["DISCORD"]["TOKEN"]
    async with ClientSession() as our_client, asyncpg.create_pool(user=USER, command_timeout=30) as pool:
        async with ReinBot(commands.when_mentioned, db_pool=pool, web_client=our_client, testing_guild_id=842248294783516673) as bot:
            await bot.start(TOKEN) 


asyncio.run(main())
