from DBHelper import DBHelper
import discord
import warnings
from commands import HelpCommand, RunCommand, LeaderboardCommand, LevelboardCommand, ProfileCommand, RecentCommand

# PortalBot V0.3.3

# Points Pre-Setup
dbHelper = DBHelper()
client = discord.Client()

# Suppress FutureWarning in console from pandas
warnings.simplefilter(action='ignore', category=FutureWarning)


@client.event
async def on_ready():
    print('Successfully logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    # If message is from bot, don't do anything
    if message.author == client.user:
        return

    command = message.content.split(" ")[0].lower()
    args = message.content.split(" ")[1:]

    if message.content.startswith('!'):
        print(f'{message.author} executed command {message.content}')

    if command.startswith('!help'):
        await HelpCommand.on_command(message, args)

    # Run Command
    if command.startswith('!run'):
        await RunCommand.on_command(message, args)

    # General Points Leaderboard Commands
    if command.startswith('!leaderboard') or command.startswith('!lb'):
        await LeaderboardCommand.on_command(message, args)

    # Chamber Points Leaderboard Commands
    if command.startswith('!levelboard') or command.startswith('!lvlb'):
        await LevelboardCommand.on_command(message, args)

    # Profile Commands
    if command.startswith('!profile') or command.startswith('!pf'):
        await ProfileCommand.on_command(message, args)

    # Recent Command
    if command.startswith('!recent'):
        await RecentCommand.on_command(message, args)

client.run(open("botToken.txt", "r").read())
