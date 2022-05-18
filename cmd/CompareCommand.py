import discord
from discord.ext import commands
from utils import DatabaseUtils


class CompareCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def compare(self, ctx):
        args = ctx.message.content.split(' ')

        if len(args) < 2:
            await ctx.send()
            return

        embed = discord.Embed()
        runners = [DatabaseUtils.get_runner_from_name(args[1]), DatabaseUtils.get_runner_from_name(args[2])]

        embed.title = f'Comparing {runners[0].speedrun_username} and {runners[1].speedrun_username}'
        embed.__setattr__('color', 0x00ffff)

        for r in runners:
            embed.add_field(name=f'{r.speedrun_username}:',
                            value=f'> Run Count: **{r.run_count()}**\n'
                                  f'> Best Category: **{r.highest_points()}**\n> \n'
                                  f'> Overall Points: **{r.points_overall}**\n'
                                  f'> Average Points: **{r.avg_points():.2f}**\n'
                                  f'> Points Glitchless: **{r.points_glitchless}**\n'
                                  f'> Points Inbounds: **{r.points_inbounds}**\n'
                                  f'> Points Out of Bounds: **{r.points_oob}**\n> \n'
                                  f'> Rank Overall: **{r.rank_overall}**\n'
                                  f'> Rank Glitchless: **{r.rank_glitchless}**\n'
                                  f'> Rank Inbounds: **{r.rank_inbounds}**\n'
                                  f'> Rank Out of Bounds: **{r.rank_oob}**')

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(CompareCommand(client))
