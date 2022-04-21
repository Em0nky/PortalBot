import discord

from utils import BotUtils, ImageUtils


async def on_command(event, args):

    if len(args) < 2:
        await event.channel.send('Missing arguments: `!help levelboard`')
        return

    level = args[1]

    if len(args) == 3:
        level = (args[1] + args[2]).replace(' ', '')

    category = BotUtils.input_to_category(args[0])
    level = BotUtils.input_to_chamber(level)

    if category is not None:
        if level is not None:

            ImageUtils.export_leaderboard_image(category=category, level=level, board_length=-1)
            replacement = ' ' if level.lower().startswith('adv') else '/'
            embed = discord.Embed()
            embed.title = f"{category} {level.replace('_', replacement)} Leaderboard:"
            image = discord.File('list.png')
            embed.set_image(url='attachment://list.png')
            await event.channel.send(embed=embed, file=image)

        else:
            await event.channel.send('Error: Invalid chamber')

    else:
        await event.channel.send('Error: Invalid category')
