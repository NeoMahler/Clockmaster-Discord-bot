import discord
from discord.ext import commands

from dotenv import load_dotenv

import logging
import os
import json

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    prefixes = ['!']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # DM commands can go without prefix
        return ['!', '']

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Modules to be loaded, following the folder.file format
initial_extensions = ['modules.bot_admin',
                      'modules.utilities',
                      'modules.night',
                      'modules.controller',
                      'modules.tools',
                      'modules.pregame',
                      'modules.game_admin'
                      ]

intents = discord.Intents(messages=True, message_content=True, members=True, guilds=True)
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

bot.remove_command('help')

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for role in os.listdir("./roles"):  # Import all roles
        if role.endswith(".py"):
            bot.load_extension(f"roles.{role[:-3]}")

    for extension in initial_extensions:
        bot.load_extension(extension)

def load_config(file_path):
    with open(file_path, 'r') as f:
        config = json.load(f)
    return config

def setup_game_status():
    starting_dictionary = {"players": {}, "day": {}, "night": {}, "status": "off"}
    with open("config/game_state.json", 'w') as f:
        json.dump(starting_dictionary, f)

@bot.event
async def on_ready():
    config = load_config('config/bot_config.json')
    bot.config = config
    bot.lang = config['language']

    if not os.path.exists("config/game_state.json"):
        print("No config/game_state.json file found. Creating one...")
        setup_game_status()

    print(f'\n\nLogged in as: {bot.user.name} - ID: {bot.user.id}\nPycord version: {discord.__version__}\n')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='ominous music...'))
    print(f'Successfully logged in and booted...!\n')

load_dotenv()
try:
    bot.run(os.environ['TOKEN'], reconnect=True)
except KeyError:
    token = input("I can't find the token. You can enter it manually here: ")
    bot.run(token, reconnect=True)
