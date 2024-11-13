import discord
from discord.ext import commands

# Replace 'TOKEN_HERE' with your bot's token
TOKEN = 'TOKEN_HERE'
PREFIX = '!'
bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

# Set intents to access members and messages
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True

# Event when bot is ready
@bot.event
async def on_ready():
    activity = discord.Game(f"Listening to my owner")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f'{bot.user} has connected to Discord!')

# Error handling for invalid commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"{ctx.author.mention}, command not found. Please check the command and try again!")

# Run the bot
bot.run(TOKEN)
