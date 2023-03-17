from discord.ext import commands
import discord
import asyncio

# import configparser

admins = [943928873412870154, 409994220309577729, 852797584812670996]

class _commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # config = configparser.ConfigParser()
    # config.read('_ventV2.0/config.ini')
    @commands.command()
    async def ping(self, ctx): 
        await ctx.send(f'Pong! In `{round(self.bot.latency * 1000)}ms`')

    @commands.Cog.listener()
    async def on_message(self, message): 
        if self.bot.user.mentioned_in(message): 
            await message.reply("prefix defined `.`")

async def setup(bot):
    await bot.add_cog(_commands(bot))
