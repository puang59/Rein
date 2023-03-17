from discord.ext import commands
import discord
import asyncio
import configparser

description = '''
Hello! I am a personal bot written by puang59 for testing purposes
'''

intents = discord.Intents.all()
intents.members = True

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config["DISCORD"]["TOKEN"]

class ReinBot(commands.Bot): 
    def __init__(self): 
        super().__init__(command_prefix="?", intents=intents)

    global check_if_allowed
    def check_if_allowed(ctx): 
        admins = [852797584812670996]
        return ctx.author.id in admins

    async def on_ready(self):
        print(f"Logged in as {bot.user} (ID: {bot.user.id})")
        print('--------')

bot = ReinBot()

@bot.command(description="Replies with pong")
@commands.check(check_if_allowed)
async def latency(ctx): 
    await ctx.send(f"{round(bot.latency * 1000)}ms")

bot.run(TOKEN)

