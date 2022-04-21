import discord

import DBHelper
from utils import ImageUtils, BotUtils


async def on_command(event, args):

    board_length = -1

    if len(args) == 1:
        if args[0].isnumeric():

            board_length = int(args[0])

            if DBHelper.leaderboard_max_length() <= board_length > 0:

                ImageUtils.export_leaderboard_image(board_length=board_length)
                embed = discord.Embed()
                embed.title = f'Top {board_length} Overall Players:'
                image = discord.File('list.png')
                embed.set_image(url='attachment://list.png')
                await event.channel.send(embed=embed, file=image)

            else:
                await event.channel.send('Error: Invalid leaderboard length.')

        else:

            if args[0].lower() == "max":

                ImageUtils.export_leaderboard_image(board_length=board_length)
                embed = discord.Embed()
                embed.title = 'All Overall Players:'
                image = discord.File('list.png')
                embed.set_image(url='attachment://list.png')
                await event.channel.send(embed=embed, file=image)

            else:

                category = BotUtils.inputToCategory(args[0])

    board_created = DBHelper.leaderboardCommand(args)

    if board_created.lower().startswith("top") or board_created.lower().startswith("all"):

        # List Image
        file = discord.File("list.png")
        embed = discord.Embed(description=f"**{board_created}**")
        embed.set_image(url="attachment://list.png")
        await event.channel.send(embed=embed, file=file)

    else:
        await event.channel.send(board_created)