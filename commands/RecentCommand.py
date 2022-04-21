import discord

import DBHelper


async def on_command(event, args):

    if len(args) == 0:
        pass

    if len(args) == 1:

        player = args[0]


    try:

        recentCreated = DBHelper.recentCommand(args)
        file = discord.File("list.png")

        if len(recentCreated) == 1:
            embed = discord.Embed(description=f"**{recentCreated[0]}'s Recent 10 Overall Runs:**")
            embed.set_image(url="attachment://list.png")
            await event.channel.send(embed=embed, file=file)

        elif len(recentCreated) == 2:
            embed = discord.Embed(description=f"**{recentCreated[0]}'s Recent 10 {recentCreated[1]} Runs:**")
            embed.set_image(url="attachment://list.png")
            await event.channel.send(embed=embed, file=file)

        else:
            if recentCreated == 'srcfail':
                await event.channel.send('Error Retrieving Submission.')

            elif recentCreated == 'catfail':
                await event.channel.send('Invalid Category.')

            else:
                await event.channel.send('Invalid Recent Command.')

    except:
        await event.channel.send('Invalid Recent Command.')