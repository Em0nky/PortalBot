import discord

import DBHelper


async def on_command(event, args):

    board_created = DBHelper.leaderboardCommand(args)

    if board_created.lower().startswith("top") or board_created.lower().startswith("all"):

        # List Image
        file = discord.File("list.png")
        embed = discord.Embed(description=f"**{board_created}**")
        embed.set_image(url="attachment://list.png")
        await event.channel.send(embed=embed, file=file)

    else:
        await event.channel.send(board_created)