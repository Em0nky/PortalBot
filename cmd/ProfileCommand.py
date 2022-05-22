import discord
from discord.ext import commands
from utils import DatabaseUtils, ImageUtils


class ProfileCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['pf'])
    async def profile(self, ctx):

        args = ctx.message.content.split(' ')
        embed = discord.Embed()
        embed.__setattr__('color', 0x00ffff)

        if len(args) == 1:

            try:
                connected_runner = DatabaseUtils.get_runner_from_discord_id(ctx.author.id)
            except TypeError:
                await ctx.send('You don\'t have an account connected. Connect using `!connect [username]`\n'
                               'To view someone else\'s profile, please use `!pf [username]`')
                return

            ImageUtils.export_image_profile(connected_runner.speedrun_username)
            embed.title = f'Profile from {connected_runner.speedrun_username}'
            embed.description = f'Overall Rank: **{connected_runner.rank_overall}** | Overall Points: **{connected_runner.points_overall}** | Average Points: **{connected_runner.avg_points():.2f}**'
            embed.set_thumbnail(url=f'https://www.speedrun.com/userasset/{connected_runner.speedrun_id}/image?v=3d18eec')

            if connected_runner.points_oob != 0:
                embed.add_field(name='**Out of Bounds:**',
                                value=f'> Points: {connected_runner.points_oob}\n'
                                      f'> Place: {connected_runner.rank_oob}')

            if connected_runner.points_inbounds != 0:
                embed.add_field(name='**Inbounds:**',
                                value=f'> Points: {connected_runner.points_inbounds}\n'
                                      f'> Place: {connected_runner.rank_inbounds}')

            if connected_runner.points_glitchless != 0:
                embed.add_field(name='**Glitchless:**',
                                value=f'> Points: {connected_runner.points_glitchless}\n'
                                      f'> Place: {connected_runner.rank_glitchless}')

            file = discord.File('list.png')
            embed.set_image(url='attachment://list.png')
            await ctx.send(embed=embed, file=file)

        else:

            try:
                player = DatabaseUtils.get_runner_from_name(args[1])
            except TypeError:
                await ctx.send(f'Runner with username `{args[1]}` not found.')
                return

            ImageUtils.export_image_profile(player.speedrun_username)
            embed.title = f'Profile from {player.speedrun_username}:'
            embed.description = f'Overall Rank: **{player.rank_overall}** | Overall Points: **{player.points_overall}** | Average Points: **{player.avg_points():.2f}**'

            embed.set_thumbnail(url=f'https://www.speedrun.com/userasset/{player.speedrun_id}/image?v=3d18eec')

            if player.points_oob != 0:
                embed.add_field(name='**Out of Bounds:**',
                                value=f'> Points: {player.points_oob}\n'
                                      f'> Place: {player.rank_oob}')

            if player.points_inbounds != 0:
                embed.add_field(name='**Inbounds:**',
                                value=f'> Points: {player.points_inbounds}\n'
                                      f'> Place: {player.rank_inbounds}')

            if player.points_glitchless != 0:
                embed.add_field(name='**Glitchless:**',
                                value=f'> Points: {player.points_glitchless}\n'
                                      f'> Place: {player.rank_glitchless}')

            file = discord.File('list.png')
            embed.set_image(url='attachment://list.png')
            await ctx.send(embed=embed, file=file)


def setup(client):
    client.add_cog(ProfileCommand(client))
