import discord


async def on_command(event, args):

    if len(args) == 0:

        embed = discord.Embed()
        embed.__setattr__('color', 0x00ffff)
        embed.title = 'PORTAL BOT'
        embed.description = '**Bot to incentivize IL runs** » [GitHub](https://github.com/Em0nky/PortalBot)\n\n' \
                            '`!leaderboard` - Display a particular leaderboard\n' \
                            '`!levelboard` - Display a particular level leaderboard\n' \
                            '`!profile` - Get different information of a specific runner\n' \
                            '`!recent` - Get the 10 most recent IL runs from a runner\n' \
                            '`!run` - Get a specific IL run from runner\n\n' \
                            '» For help for a specific command use `!help [command]`'

        await event.channel.send(embed=embed)

    else:

        if args[0].lower() == 'leaderboard' or args[0].lower() == 'lb':

            embed = discord.Embed()
            embed.__setattr__('color', 0x00ffff)
            embed.title = 'Help: !leaderboard Command'
            embed.add_field(name="!leaderboard",
                            value="This returns an overall points leaderboard of the top 10 runners.",
                            inline=False)
            embed.add_field(name="!leaderboard max",
                            value="This returns an overall points leaderboard of all runners. (This is really tall)",
                            inline=False)
            embed.add_field(name="!leaderboard [number]",
                            value="This returns an overall points leaderboard of the top [number] runners.",
                            inline=False)
            embed.add_field(name="!leaderboard [category]",
                            value="This returns a points leaderboard of the top 10 [category] runners.",
                            inline=False)
            embed.add_field(name="!leaderboard [category] [number]",
                            value="This returns a points leaderboard of the top [number] [category] runners.",
                            inline=False)

            await event.channel.send(embed=embed)

        elif args[0].lower() == 'levelboard' or args[0].lower() == 'lvlb':

            embed = discord.Embed()
            embed.__setattr__('color', 0x00ffff)
            embed.title = 'Help: !levelboard Command'
            embed.add_field(name="!levelboard [category] [level]",
                            value="This returns the points leaderboard of [level] in [category].",
                            inline=False)

            await event.channel.send(embed=embed)

        elif args[0].lower() == "profile" or args[0].lower() == 'pf':

            embed = discord.Embed()
            embed.__setattr__('color', 0x00ffff)
            embed.title = 'Help: !profile Command'
            embed.add_field(name="!profile",
                            value="This returns a linked user's top 5 runs and total points. **NOT IMPLEMENTED**",
                            inline=False)
            embed.add_field(name="!profile [player]",
                            value="Display [player]'s profile. Top 5 runs, overall & category stats.",
                            inline=False)
            embed.add_field(name="!profile [player] [category]",
                            value="This returns the [player]'s top 10 runs in [category], overall place and points.",
                            inline=False)
            embed.add_field(name="!profile [player] [category] all",
                            value="This returns all of [players]'s runs in [category], overall place and points.",
                            inline=False)

            await event.channel.send(embed=embed)

        elif args[0].lower() == "run":

            embed = discord.Embed()
            embed.__setattr__('color', 0x00ffff)
            embed.title = 'Help: !run Command'
            embed.add_field(name="!run [player] [category] [chamber]",
                            value="This returns [player's] run of [category] in [chamber]",
                            inline=False)

            await event.channel.send(embed=embed)

        elif args[0].lower() == "recent":

            embed = discord.Embed()
            embed.__setattr__('color', 0x00ffff)
            embed.title = 'Help: !recent Command'
            embed = discord.Embed()
            embed.add_field(name="!recent [player]",
                            value="This returns [player]'s 10 most recent ILs.",
                            inline=False)
            embed.add_field(name="!recent [player] [category]",
                            value="This returns [player]'s 10 most recent ILs in a specific category.",
                            inline=False)

            await event.channel.send(embed=embed)

        else:

            await event.channel.send('Command not found')


class HelpCommand:
    pass
