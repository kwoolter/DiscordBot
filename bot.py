# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ROLE_GAMER = os.getenv('DISCORD_ROLE_GAMER')
CHANNEL_GAME = os.getenv('DISCORD_CHANNEL_GAME')

intents = discord.Intents(members=True, guilds=True)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', loop=None, fetch_offline_members=True, intents=intents)


@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)

    response = f'{bot.user} is connected to the following guild:\n' + \
               f'{guild.name}(id: {guild.id})'

    print(response)

    for channel in guild.channels:
        if channel.type == discord.ChannelType.text:
            await channel.send(response)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    response = f"Channel {message.channel.name}:{message.author} says '{message.system_content}'"
    is_to_bot = False
    is_to_game = message.channel.name == CHANNEL_GAME

    if len(message.mentions) > 0:
        response += " to "
        for i, mention in enumerate(message.mentions):
            if mention.name == bot.user.name:
                is_to_bot = True
            response += mention.name
            if i < len(message.mentions) - 1:
                response += ", "
    print(response)

    if is_to_bot is True:
        channel = message.channel
        response = f'Hello {message.author}!'
        await channel.send(response)

    if is_to_game is True:
        channel = message.channel

        embed = discord.Embed(title=f"Game BOT on Channel {message.channel.name}",
                              color=discord.Color.blue())

        embed.set_thumbnail(url="https://images.megapixl.com/2070/20707154.jpg")

        embed.add_field(name=f"Received message from {message.author.name}",
                        value=message.system_content,
                        inline=False)

        embed.set_footer(text="### END OF MESSAGE ###")

        await channel.send(embed=embed)


    await bot.process_commands(message)

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"An error occurred:{event}")
    for i,arg in enumerate(args):
        print(f'{i}:{arg}')


@bot.event
async def on_command_error(ctx, error):
    print(error)

    response = f"#{ctx.channel.name}:{ctx.author.name} tried command '{ctx.invoked_with}' and got error '{error}'!!!"
    print(response)

    await ctx.send(response)


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
@commands.has_role(ROLE_GAMER)
async def test(ctx):
    response = f"Yes, indeed {ctx.author.display_name} !"
    await ctx.send(response)


@bot.command(name='embed', help='Test out various Embed fetaures')
@commands.has_role('admin')
async def embed(ctx):
    embed = discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/",
                          description="This is an embed that will show how to build an embed and the different components",
                          color=0xFF5733)
    await ctx.send(embed=embed)


@bot.command(name='admin', help='secret admin stuff')
@commands.has_role('admin')
async def admin(ctx, admin_cmd='help'):
    response = f"Welcome master {ctx.author.display_name}. I will obey your command '{admin_cmd}'."
    await ctx.send(response)

    if admin_cmd == "1":
        guild = ctx.guild

        response = f'{ctx.bot.user} is connected to the following guild:\n' + \
                   f'{guild.name}(id: {guild.id})'

        print(response)

        for channel in guild.channels:
            if channel.type == discord.ChannelType.text:
                await channel.send(response)


@bot.command(name='server', help='Information about this server')
@commands.has_role('admin')
@commands.cooldown(rate=1,per=10,type=commands.BucketType.channel)
async def fetch_server_info(ctx):
    guild = ctx.guild

    embed = discord.Embed(title=f"Server Name: {guild.name}",
                          description=f"Owned by {guild.owner.display_name} with {len(guild.members)} members",
                          color=discord.Color.blue())

    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.set_thumbnail(url="https://images.megapixl.com/2070/20707154.jpg")

    embed.add_field(name=f"Command from {ctx.author.name}", value="This is the value for field 1. This is NOT an inline field.",
                    inline=False)
    embed.add_field(name="Field 2 Title", value="It is inline with Field 3", inline=True)
    embed.add_field(name="Field 3 Title", value="It is inline with Field 2", inline=True)

    embed.set_footer(text="### END OF MESSAGE ###")

    await ctx.send(embed=embed)

bot.run(TOKEN)
