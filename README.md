# DiscordBot
Create a basic Discord bot using `discord.py` based on the realpython tutorial.

## Features
* `on_ready` - the bot starts up
* `on_message` - handling message events
    * Different behaviour based on the channel that the message was received on
    * Different behaviour if the Bot was mentioned in the message
* Command events - process user-defined commands
    * Permissions using `commands.has_role()`
    * Cooldowns using `commands.cooldown()`
* `Embed` - nicely formatted responses from the bot
* Error Handling
    * `on_error`
    * `on_command_error` - an error processing a command
 
## Dependencies
* `discord.py`
* `python-dotenv`

## `.env` File
You will need to create you own `.env` file with the following environment variables defined:

```
DISCORD_TOKEN={ complete }
DISCORD_GUILD={ complete }
DISCORD_ROLE_GAMER=gamer
DISCORD_CHANNEL_GAME=game
```

# References
* https://realpython.com/how-to-make-a-discord-bot-python/ - tutorial for setting up a bot
* https://discordpy.readthedocs.io/en/latest/index.html - `disord.py` API reference guide
* https://discord.com/developers/applications - Discord developers' portal
