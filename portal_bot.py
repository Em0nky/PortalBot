import os
import warnings

from discord.ext import commands

# PortalBot v1.0
from discord.ext.commands import CommandNotFound

client = commands.Bot(command_prefix='!')

# Suppress FutureWarning in console from pandas
warnings.simplefilter(action='ignore', category=FutureWarning)
# Suppress SQLAlchemy related UserWarning in console from pandas
warnings.simplefilter(action='ignore', category=UserWarning)


@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user}')


@client.event
async def on_message(message):
    await client.process_commands(message)


for filename in os.listdir('./cmd'):
    if filename.endswith('.py') and filename != '__init__.py':
        client.load_extension(f'cmd.{filename[:-3]}')
        print(f'Loaded cmd.{filename[:-3]}')

client.run(open('token.txt', 'r').read())
