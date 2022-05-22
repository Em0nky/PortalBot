import discord
from discord.ext import commands
from utils import ImageUtils, BotUtils


def detect_map_in_args(args):
    for a in args:
        if BotUtils.input_to_chamber(a) is not None:
            return a


def detect_category_in_args(args):
    for a in args:
        if BotUtils.input_to_category(a) is not None:
            return a


class LeaderboardCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['lb', 'lvlb', 'levelboard'])
    async def leaderboard(self, ctx):

        args = ctx.message.content.split(' ')

        if len(args) == 1:

            ImageUtils.export_image_leaderboard()

            embed = discord.Embed()
            embed.__setattr__('color', 0x00ffff)
            embed.title = 'Top 10 __Overall__ Leaderboard'
            image = discord.File('list.png')
            embed.set_image(url='attachment://list.png')

            await ctx.send(embed=embed, file=image)

        elif len(args) == 2:

            category = BotUtils.input_to_category(args[1])

            match category:
                case 'Inbounds':
                    ImageUtils.export_image_leaderboard(ImageUtils.BoardSortValue.points_inbounds)
                case 'Glitchless':
                    ImageUtils.export_image_leaderboard(ImageUtils.BoardSortValue.points_glitchless)
                case 'Out_of_Bounds':
                    ImageUtils.export_image_leaderboard(ImageUtils.BoardSortValue.points_oob)
                case _:
                    await ctx.send('Invalid category, please use `Inbounds`, `OoB` or `Glitchless`')
                    return

            embed = discord.Embed()
            embed.__setattr__('color', 0x00ffff)
            embed.title = f'Top 10 __{category.replace("_", " ")}__ Leaderboard'
            image = discord.File('list.png')
            embed.set_image(url='attachment://list.png')

            await ctx.send(embed=embed, file=image)

        elif len(args) == 3:

            category = BotUtils.input_to_category(detect_category_in_args(args))
            level = BotUtils.input_to_chamber(detect_map_in_args(args))

            if category is None:
                await ctx.send('Invalid category, please use `Inbounds`, `OoB` or `Glitchless`')
                return

            if level is None:
                await ctx.send(f'{args[2]} is not a valid level.')
                return

            ImageUtils.export_image_level(category, level)

            embed = discord.Embed()
            embed.__setattr__('color', 0x00ffff)
            embed.title = f'Top 10 __{level}: {category.replace("_", " ")}__ Leaderboard'
            image = discord.File('list.png')
            embed.set_image(url='attachment://list.png')

            await ctx.send(embed=embed, file=image)

        elif len(args) == 4:

            if args[3].startswith('filter='):

                result_filter = args[3].replace('filter=', '')
                category = BotUtils.input_to_category(detect_category_in_args(args))
                level = BotUtils.input_to_chamber(detect_map_in_args(args))

                if category is None:
                    await ctx.send('Invalid category, please use `Inbounds`, `OoB` or `Glitchless`')
                    return

                if level is None:
                    await ctx.send(f'{args[2]} is not a valid level.')
                    return

                ImageUtils.export_image_level(category, level, result_filter=result_filter)

                embed = discord.Embed()
                embed.__setattr__('color', 0x00ffff)
                embed.title = f'__{level}: {category.replace("_", " ")}__ Leaderboard (`filter={result_filter}`)'
                image = discord.File('list.png')
                embed.set_image(url='attachment://list.png')

                await ctx.send(embed=embed, file=image)


def setup(client):
    client.add_cog(LeaderboardCommand(client))
