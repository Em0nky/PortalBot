import discord

from DBHelper import DBHelper


async def on_command(event, args):

    if len(args) < 2:
        await event.channel.send('Missing arguments: `!help levelboard`')

    dbHelper = DBHelper()
    board_created = dbHelper.levelboardCommand(args)

    if board_created.startswith('Error'):
        await event.channel.send(board_created)
        return

    file = discord.File("list.png")
    embed = discord.Embed(description=f"**{board_created}**")
    embed.set_image(url="attachment://list.png")
    await event.channel.send(embed=embed, file=file)
