import discord

from DBHelper import DBHelper
from utils import BotUtils


async def on_command(event, args):

    dbHelper = DBHelper()
    profile_created = dbHelper.userprofileCommand(args)

    if len(profile_created) == 4:
        playerID = str(profile_created[2])
        playerName = str(profile_created[3])
        profileCreatedS = profile_created[0] + profile_created[1]
        profileCreatedS = profileCreatedS.split(",")

        file = discord.File("list.png")
        embed = BotUtils.embedProfile(args, profileCreatedS, playerID, playerName)
        embed.set_image(url="attachment://list.png")
        await event.channel.send(embed=embed, file=file)

    elif len(profile_created) == 3:

        playerID = str(profile_created[1])
        playerName = str(profile_created[2])
        profileCreatedS = profile_created[0]
        profileCreatedS = profileCreatedS.split(",")

        file = discord.File("list.png")
        embed = BotUtils.embedProfile(args, profileCreatedS, playerID, playerName)
        embed.set_image(url="attachment://list.png")
        await event.channel.send(embed=embed, file=file)

    elif profile_created.startswith('Error'):
        await event.channel.send(profile_created)
