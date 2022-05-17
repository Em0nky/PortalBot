import discord
from discord.ext import commands


class HelpCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['h'])
    async def help(self, ctx):

        args = ctx.message.content.split(' ')
        embed = discord.Embed()
        embed.__setattr__('color', 0x00ffff)
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/916508398810443887/337379def5e16409c76e59856048a084.png')

        if len(args) == 1:

            embed.title = 'PORTAL BOT'
            embed.description = '**Bot to incentivize IL runs** » [Leaderboard](https://www.speedrun.com/portal/levels) - [Contribute](https://github.com/Em0nky/PortalBot)\n\n' \
                                '`!leaderboard` - Display a leaderboard.\n' \
                                '`!connect` - Connect your speedrun.com profile.\n' \
                                '`!profile` - View profile from a specified runner.\n' \
                                '`!convert` - Convert between time and ticks.\n' \
                                '`!recent` - Get the 10 most recent IL runs from a runner.\n' \
                                '`!run` - Get a specific IL run from runner\n\n' \
                                '» For help for a specific command use `!help [command]`'

        else:

            if args[1].lower() == 'leaderboard' or args[1].lower() == 'lb':
                embed.title = 'Help: !leaderboard Command'
                embed.description = 'Aliases: `!lb`, `!lvlb`, `!levelboard`'
                embed.add_field(name='!leaderboard',
                                value='Displays an overall points leaderboard of the top 10 runners.\n'
                                      '> Example: `!leaderboard`',
                                inline=False)
                embed.add_field(name='!leaderboard [category]',
                                value='Displays a leaderboard of the top 10 [category] runners.\n'
                                      '> Example: `!leaderboard inbounds`',
                                inline=False)
                embed.add_field(name='!leaderboard [category] [level]',
                                value='Displays a leaderboard of the top [level] [category] runners.\n'
                                      '> Example: `!leaderboard oob 14`',
                                inline=False)
                embed.add_field(name='!leaderboard [category] [level] [filter=?]',
                                value='Displays a level leaderboard with filtered output.\n'
                                      '> Example: `!leaderboard oob 14 filter=place>1`',
                                inline=False)

            if args[1].lower() == 'profile' or args[1].lower() == 'pf':
                embed.title = 'Help: !profile Command'
                embed.description = 'Aliases: `!pf`'
                embed.add_field(name='!profile',
                                value='Requires connected account: Display your profile.',
                                inline=False)
                embed.add_field(name='!profile [player]',
                                value='Display [player]\'s profile.',
                                inline=False)

            if args[1].lower() == 'run':
                embed.title = 'Help: !run Command'
                embed.add_field(name='!run [player] [category] [chamber]',
                                value='Display [player]\'s run of [chamber] in [category] ',
                                inline=False)

            if args[1].lower() == 'recent':
                embed.title = 'Help: !recent Command'
                embed.add_field(name='!recent [player]',
                                value='Display a list of [player]\'s 10 most recent ILs.',
                                inline=False)
                embed.add_field(name='!recent [player] [category]',
                                value='Display a list of [player]\'s 10 most recent ILs in specified category.',
                                inline=False)

            if args[1].lower() == 'convert':
                embed.title = 'Help: !convert Command'
                embed.add_field(name='!convert [time/ticks]',
                                value='Convert ticks or time to their respective format.',
                                inline=False)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(HelpCommand(client))
