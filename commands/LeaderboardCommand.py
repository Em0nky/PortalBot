import discord

import DBHelper
from utils import ImageUtils, BotUtils


async def on_command(event, args):
    board_length = -1

    if len(args) == 1:
        if args[0].isnumeric():

            board_length = int(args[0])

            if DBHelper.leaderboard_max_length() >= board_length > 0:

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

                category = BotUtils.input_to_category(args[0])

                if category is not None:

                    ImageUtils.export_leaderboard_image(category=category)
                    embed = discord.Embed()
                    embed.title = f'Top {category} Players:'
                    image = discord.File('list.png')
                    embed.set_image(url='attachment://list.png')
                    await event.channel.send(embed=embed, file=image)

                else:
                    await event.channel.send('Error: Invalid category')

    elif len(args) == 2:

        category = BotUtils.input_to_category(args[0])
        board_length = -1

        if not args[1].lower() == "max":
            board_length = int(args[1])

        ImageUtils.export_leaderboard_image(category=category, board_length=board_length)
        embed = discord.Embed()
        embed.title = f"Top {board_length if not board_length == -1 else ''} {category} Players"
        image = discord.File('list.png')
        embed.set_image(url='attachment://list.png')
        await event.channel.send(embed=embed, file=image)

    else:

        ImageUtils.export_leaderboard_image()
        embed = discord.Embed()
        embed.title = 'Top Overall Players'
        image = discord.File('list.png')
        embed.set_image(url='attachment://list.png')
        await event.channel.send(embed=embed, file=image)
