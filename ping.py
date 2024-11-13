import discord
from discord.ext import commands
import time

# Store the time when the bot started
start_time = time.time()

async def ping(ctx):
    # Calculate bot latency (Time it takes for the bot to respond to a command)
    latency = round(ctx.bot.latency * 1000)  # Convert to ms
    
    # Calculate the API latency (This is the time it takes for Discord to respond to the bot)
    api_latency = round((time.time() - start_time) * 1000)  # Time since bot started, in ms
    
    # Get bot uptime
    uptime = str(time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))
    
    # Get the number of servers the bot is in
    guild_count = len(ctx.bot.guilds)
    
    # Get the number of users the bot is serving
    user_count = sum(guild.member_count for guild in ctx.bot.guilds)
    
    # Create an embed for a clean presentation
    embed = discord.Embed(title="Bot Status", description="Here's the current status of the bot.", color=discord.Color.green())
    
    # Add fields to the embed
    embed.add_field(name="Ping (Bot to Discord)", value=f"{latency} ms", inline=False)
    embed.add_field(name="API Latency", value=f"{api_latency} ms", inline=False)
    embed.add_field(name="Uptime", value=uptime, inline=False)
    embed.add_field(name="Servers", value=f"{guild_count} servers", inline=False)
    embed.add_field(name="Users", value=f"{user_count} users", inline=False)
    
    # Send the embed message
    await ctx.send(embed=embed)
