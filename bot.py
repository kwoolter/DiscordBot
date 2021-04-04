# bot.py
import os

import discord
from discord.ext import commands


from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
active_guild = None
bot = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    global active_guild

    for guild in client.guilds:
        if guild.name == GUILD:
            active_guild = guild
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    text_channel_list = []
    for channel in guild.channels:
        if channel.type == discord.ChannelType.text:
            text_channel_list.append(channel)
            await channel.send("bot is online")

    print(f'Channels:{text_channel_list}')

@client.event
async def on_error():
    for channel in active_guild.channels:
        if channel.type == discord.ChannelType.text:
            await channel.send("bot error")

@bot.command()
async def test(ctx, arg):
    print(f'Test comand: input={arg}')
    await ctx.send(arg)


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

client.run(TOKEN)

