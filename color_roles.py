import discord
import re
from discord.ext import commands

# Regular expression to validate hex color codes
HEX_COLOR_REGEX = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')

# Map common color names to hex codes
COLOR_NAMES = {
    "pink": "#FFC0CB",
    "red": "#FF0000",
    "blue": "#0000FF",
    "green": "#008000",
    "yellow": "#FFFF00",
    "purple": "#800080",
    "orange": "#FFA500",
    "black": "#000000",
    "white": "#FFFFFF",
}

# Function to allow users to change their color
async def change_color(ctx, color: str):
    # If color is a name, look up its hex code
    if color.lower() in COLOR_NAMES:
        color = COLOR_NAMES[color.lower()]

    # Check if the color is a valid hex code
    if not HEX_COLOR_REGEX.match(color):
        await ctx.send("Invalid color! Please provide a valid hex code (e.g., #FF5733) or color name (e.g., pink, red).")
        return

    # Convert the hex color to an integer for Discord's color format
    color_value = int(color[1:], 16)

    # Check if the user already has a color role
    existing_role = discord.utils.find(lambda r: r.name == f"{ctx.author.name}'s Color", ctx.guild.roles)
    
    if existing_role:
        # Update the existing role with the new color
        await existing_role.edit(color=discord.Color(color_value))
        await ctx.send(f"Your color has been updated to {color}!")
    else:
        # Create a new role with the specified color if one does not exist
        try:
            new_role = await ctx.guild.create_role(
                name=f"{ctx.author.name}'s Color",
                color=discord.Color(color_value),
                reason="User color customization"
            )

            # Ensure the bot has the necessary permissions
            if not ctx.guild.me.guild_permissions.manage_roles:
                await ctx.send("I do not have permission to manage roles.")
                return

            # Get the user's highest role
            highest_role = ctx.author.top_role

            # Position the new role above the user's highest role
            await new_role.edit(position=highest_role.position + 1)

            # Add the newly created role to the user
            await ctx.author.add_roles(new_role)
            await ctx.send(f"Your color has been set to {color}.")

        except discord.Forbidden:
            await ctx.send("I do not have permission to create roles.")
            print("Bot does not have permission to create roles.")
    
    # Remove old color roles ONLY if they are not the newly created role
    for role in ctx.author.roles:
        if role != existing_role and role.name.endswith("Color") and role != ctx.guild.default_role and role != new_role:
            await role.delete(reason="Cleanup of previous color role")
