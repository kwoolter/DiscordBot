# bot.py
import os
import random
from dotenv import load_dotenv

import discord
from discord.ext import commands, tasks


# Load in all of the environment variables that we are going to use
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ROLE_GAMER = os.getenv('DISCORD_ROLE_GAMER')
CHANNEL_GAME = os.getenv('DISCORD_CHANNEL_GAME')

# Create a Bot instance
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', loop=None, fetch_offline_members=True, intents=intents)
game_channel = None

@bot.event
async def on_ready():
    """
    Event when the bot is started and ready to go!
    """
    global game_channel

    # Change the bot's status
    await bot.change_presence(activity=discord.Game('My new BOT game'))

    # Get the server that we are interested in based on the config
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)

    # Build a basic response message
    response = f'{bot.user} is connected to the following guild:\n' + \
               f'{guild.name}(id: {guild.id})'

    print(response)

    # Loop through all of the channels on the server
    for channel in guild.channels:

        # If this is a text channel...
        if channel.type == discord.ChannelType.text:

            # Post a connection message onto the channel
            await channel.send(response)

            # If this is the configured game channel then add special Embed message
            if channel.name == CHANNEL_GAME:
                game_channel = channel

                embed = discord.Embed(title=f"Game BOT on Channel #{channel.name}",
                                      color=discord.Color.blue())

                embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
                embed.set_thumbnail(url="https://images.megapixl.com/2070/20707154.jpg")

                embed.add_field(name=f"I'm on-line!",
                                value="I'm listening on this channel for game related messages!",
                                inline=False)

                embed.set_footer(text="### END OF MESSAGE ###")

                await channel.send(embed=embed)

    # Start the timers
    timer5.start()

@bot.event
async def on_user_update(before, after):
    print(f'{before} -> {after}')

@bot.event
async def on_member_update(before, after):
    """
    Process event when a memeber of the server updates themselves
    :param before: before Member
    :param after:  after Member
    """

    if before.status != after.status:

        if after.status == discord.Status.idle:
            response = f'Wakey Wakey {after.name}'
        elif after.status == discord.Status.offline:
            response = f"Goodbye {after.name}, see you later!"
        else:
            response = f'Member {after.name} status is now {after.status}'

        print(response)
        await game_channel.send(response)


@bot.event
async def on_message(message):
    """
    Process a new message that has been send to the server
    :param message: the message object that was sent
    :return:
    """

    # If this messages if from this Bot then exit
    if message.author == bot.user:
        return

    response = f"Channel {message.channel.name}:{message.author} says '{message.system_content}'"

    # Assume message not sent to bot
    is_to_bot = False

    # Set flag if this message was received on teh game channel
    is_to_game = message.channel.name == CHANNEL_GAME

    # If Guild Members were mentioned in the message...
    if len(message.mentions) > 0:
        response += " to "
        for i, mention in enumerate(message.mentions):

            # If this bot was mentioned then set a flag
            if mention.name == bot.user.name:
                is_to_bot = True

            # Add the member to the response
            response += mention.name
            if i < len(message.mentions) - 1:
                response += ", "

    print(response)

    # If this message was send to this bot...
    if is_to_bot is True:
        channel = message.channel
        response = f'Hello {message.author}!'
        await channel.send(response)

    # If this message was sent on the game channel...
    if is_to_game is True:

        # Build a special Embed response for messages sent on the game channel

        channel = message.channel

        embed = discord.Embed(title=f"Game BOT on Channel #{message.channel.name}",
                              color=discord.Color.blue())

        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

        embed.set_thumbnail(url="https://images.megapixl.com/2070/20707154.jpg")

        embed.add_field(name=f"Received message from {message.author.name}",
                        value=message.system_content,
                        inline=False)

        embed.set_footer(text="### END OF MESSAGE ###")

        await channel.send(embed=embed)

    # Process commands if this message was a command
    await bot.process_commands(message)

@bot.event
async def on_error(event, *args, **kwargs):
    """
    Process an error event
    :param event: The event that has occurred
    :param args:
    :param kwargs:
    """

    # Print out the error and any arguments
    print(f"An error occurred:{event}")
    for i,arg in enumerate(args):
        print(f'{i}:{arg}')


@bot.event
async def on_command_error(ctx, error):
    """
    Process a command error
    :param ctx: The context
    :param error: The error
    """
    print(error)

    response = f"#{ctx.channel.name}:{ctx.author.name} tried command '{ctx.invoked_with}' and got error '{error}'!!!"
    print(response)

    await ctx.send(response)


@tasks.loop(seconds=5.0)
async def timer5():

    response = "My 5 second timer"
    print(response)
    #await game_channel.send(response)


@bot.command(name='test', help='Call out if you want to test something', category='Group 1')
@commands.has_role(ROLE_GAMER)
async def test(ctx):
    """
    Process a test command that is only available to a specific role
    :param ctx:
    """
    response = f"Yes, indeed {ctx.author.display_name} !"
    await ctx.send(response)


@bot.command(name='embed', help='Test out various Embed fetaures')
@commands.has_role('admin')
async def embed(ctx):
    """
    Command to test Embeds
    :param ctx:
    """
    embed = discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/",
                          description="This is an embed that will show how to build an embed and the different components",
                          color=0xFF5733)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.set_thumbnail(url="https://images.megapixl.com/2070/20707154.jpg")

    embed.add_field(name=f"Command from {ctx.author.name}", value="This is the value for field 1. This is NOT an inline field.",
                    inline=False)
    embed.add_field(name="Field 2 Title", value="It is inline with Field 3", inline=True)
    embed.add_field(name="Field 3 Title", value="It is inline with Field 2", inline=True)

    embed.set_footer(text="### END OF MESSAGE ###")

    await ctx.send(embed=embed)


@bot.command(name='admin', help='secret admin stuff')
@commands.has_role('admin')
async def admin(ctx, admin_cmd='1'):
    """
    Admin command that checks parameter value e.g. !admin 1
    :param ctx:
    :param admin_cmd: Which admin command you want to execute e.g. 1
    """
    response = f"Welcome master {ctx.author.display_name}. I will obey your command '{admin_cmd}'."
    await ctx.send(response)
    guild = ctx.guild

    # If the admin command was 1...
    if admin_cmd == "1":

        # Build a response
        response = f'{ctx.bot.user} is connected to the following guild:\n' + \
                   f'{guild.name}(id: {guild.id})'

        print(response)

        # Send the response on all channels
        for channel in guild.channels:
            if channel.type == discord.ChannelType.text:
                await channel.send(response)

    # If the admin command was 2 or 3...
    elif admin_cmd in ["2", "3"]:
        response = f"Running special admin command {admin_cmd}..."
        # Send the response on all channels
        for channel in guild.channels:
            if channel.type == discord.ChannelType.text:
                await channel.send(response)


    # Else we don't recognise this admin command so respond on this channel only
    else:
        channel = ctx.channel
        response = f"Unknown admin command {admin_cmd}"
        await channel.send(response)



@bot.command(name='server', help='Information about this server')
@commands.has_role('admin')
@commands.cooldown(rate=1,per=10,type=commands.BucketType.channel)
async def fetch_server_info(ctx):
    """
    Command to print some details about the server
    :param ctx:
    """
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


# Run the bot
bot.run(TOKEN)
