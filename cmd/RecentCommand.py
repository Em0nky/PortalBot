import discord
from discord.ext import commands

from utils import DatabaseUtils, ImageUtils


class RecentCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def recent(self, ctx):

        args = ctx.message.content.split(' ')
        embed = discord.Embed()
        embed.__setattr__('color', 0x00ffff)

        if len(args) == 1:

            connected_runner = DatabaseUtils.get_runner_from_discord_id(ctx.author.id)
            embed.title = f'10 most recent runs from {connected_runner.speedrun_username}'

            if connected_runner is None:
                await ctx.send('You don\'t have an account connected. Connect using `!connect [username]`\n'
                               'To view someone else\'s profile, please use `!pf [username]`')
                return

            ImageUtils.export_image_recent(connected_runner.speedrun_username)
            file = discord.File('list.png')
            embed.set_image(url='attachment://list.png')
            await ctx.send(embed=embed, file=file)

        else:

            try:
                player = DatabaseUtils.get_runner_from_name(args[1])
            except TypeError:
                await ctx.send(f'Runner with username `{args[1]}` not found.')
                return

            ImageUtils.export_image_recent(player.speedrun_username)
            embed.title = f'10 most recent runs from {player.speedrun_username}'
            file = discord.File('list.png')
            embed.set_image(url='attachment://list.png')
            await ctx.send(embed=embed, file=file)


def setup(client):
    client.add_cog(RecentCommand(client))
