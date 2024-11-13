import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import mysql.connector
from db import get_db_cursor, close_db_connection  # Import the function to get the connection and cursor
# Import the ping command from ping.py
from ping import ping
from color_roles import change_color

# Load environment variables from .env file
load_dotenv()

# Get the database connection and cursor
db, cursor = get_db_cursor()

# Retrieve the bot's token and prefix from environment variables
TOKEN = os.getenv("BOT_TOKEN")
PREFIX = os.getenv("BOT_PREFIX")

bot = commands.Bot(command_prefix=PREFIX, help_command=None, intents=discord.Intents.all())

# Set intents to access members and messages
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True

# Event when bot is ready
@bot.event
async def on_ready():
    activity = discord.Game(f"!help")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f'{bot.user} has connected to Discord!')

@bot.command(name="changecolor", help="Change your name color by providing a hex color (e.g., #FF5733).")
async def changecolor_cmd(ctx, color: str):
    await change_color(ctx, color)

# Register the ping command
@bot.command(name="ping", help="Check the bot's latency, uptime, and server/user stats.")
async def ping_command(ctx):
    await ping(ctx)

# Error handling for invalid commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"{ctx.author.mention}, command not found. Please check the command and try again!")

@bot.event
async def on_close():
    close_db_connection(db, cursor)

# Run the bot
bot.run(TOKEN)
