# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix='!')

@client.event
async def on_ready():

    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    response = f'{client.user} is connected to the following guild:\n' + \
        f'{guild.name}(id: {guild.id})'

    print(response)

    for channel in guild.channels:
        if channel.type == discord.ChannelType.text:
            await channel.send(response)

@bot.command(name='99', help='stupid function')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='test', help='Call out is you want to test something', category='Group 1')
async def test(ctx):
    response = f"Yes, indeed {ctx.author.display_name}!"
    await ctx.send(response)


@bot.command(name='admin', help='secret admin stuff')
@commands.has_role('admin')
async def admin(ctx, admin_cmd='help'):

    response = f"Welcome master {ctx.author.display_name}. I will obey your command '{admin_cmd}'."
    await ctx.send(response)


bot.run(TOKEN)