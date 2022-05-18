from datetime import datetime
import discord
from discord.ext import commands
from utils import BotUtils, DatabaseUtils


class RunCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def run(self, ctx):
        args = ctx.message.content.split(' ')

        if len(args) < 3:
            await ctx.send('Missing arguments: `!help run`')
            return

        category = BotUtils.input_to_category(args[2])
        level = BotUtils.input_to_chamber(args[3])

        try:
            player = DatabaseUtils.get_runner_from_name(args[1])
        except TypeError:
            await ctx.send(f'Runner with username `{args[1]}` could not be found.')
            return

        if category is None:
            await ctx.send('Invalid category, please use `Inbounds`, `OoB` or `Glitchless`')
            return

        if level is None:
            await ctx.send(f'`{args[3]}` is not a valid level.')
            return

        try:
            run = DatabaseUtils.get_run_from_player(player.speedrun_username, category, level)
        except TypeError:
            await ctx.send('Run could not be found.')
            return

        embed = discord.Embed()
        run_links = f'[Run]({run.weblink})'

        if run.video is not None:
            run_links += f' | [Video]({run.video})'

        if run.demos is not None:
            run_links += f' | [Demos]({run.demos})'

        embed.title = f'{run.level}: {run.category} run by {run.speedrun_username}'
        embed.description = f'[ {run_links} ]'
        embed.__setattr__('color', 0x00ffff)
        place = '%d%s' % (run.place, {1: 'st', 2: 'nd', 3: 'rd'}.get(run.place if run.place < 20 else run.place % 10, 'th'))
        place = '%s%s' % ({1: ':trophy: ', 2: ':second_place: ', 3: ':third_place: '}.get(run.place), place)
        embed.add_field(name='**Place**', value=place.replace('None', ''), inline=True)
        embed.add_field(name='**Points**', value=str(run.points), inline=True)
        dt = datetime.fromtimestamp(run.date / 1000)
        embed.add_field(name='**Date**', value=str(dt.date()), inline=False)
        embed.add_field(name='**Time**', value=str(run.time / 1000), inline=True)
        embed.add_field(name='**Ticks**', value=f'{run.time / 15: .000f}', inline=True)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(RunCommand(client))
