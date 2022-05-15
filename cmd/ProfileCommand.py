import discord
from discord.ext import commands
from utils import DatabaseUtils, ImageUtils


class ProfileCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['pf'])
    async def profile(self, ctx):

        args = ctx.message.content.split(' ')
        player = DatabaseUtils.get_runner_from_name(args[1])

        if player is None:
            await ctx.send(f'Runner with username {args[1]} not found.')
            return

        ImageUtils.export_image_profile(player.speedrun_username)
        embed = discord.Embed()
        embed.title = f'{player.speedrun_username if player.speedrun_username.endswith("s") else player.speedrun_username + "s"} Profile:'

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

        embed.add_field(name=f'_ _', value=f'**Overall Place:** {player.rank_overall} | **Overall Points:** {player.points_overall}', inline=False)
        file = discord.File('list.png')
        embed.set_image(url='attachment://list.png')
        embed.__setattr__('color', 0x00ffff)
        await ctx.send(embed=embed, file=file)


def setup(client):
    client.add_cog(ProfileCommand(client))
