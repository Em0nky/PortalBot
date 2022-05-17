import os
import warnings

from discord.ext import commands

# PortalBot v1.0 | Developed and maintained by Em0nky and lundylizard
client = commands.Bot(command_prefix='!', help_command=None)

# Suppress FutureWarning in console from pandas
warnings.simplefilter(action='ignore', category=FutureWarning)
# Suppress SQLAlchemy related UserWarning in console from pandas
warnings.simplefilter(action='ignore', category=UserWarning)


@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user}')


# Process commands when a message was sent
@client.event
async def on_message(message):
    await client.process_commands(message)


# Load all commands as extensions for discord.py
for filename in os.listdir('./cmd'):
    if filename.endswith('.py') and filename != '__init__.py':
        client.load_extension(f'cmd.{filename[:-3]}')
        print(f'Loaded cmd.{filename[:-3]}')

# TODO read config file for bot, instead of token file
client.run(open('token.txt', 'r').read())
