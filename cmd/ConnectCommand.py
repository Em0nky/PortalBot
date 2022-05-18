from discord.ext import commands

from utils import DatabaseUtils


class ConnectCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def connect(self, ctx):

        args = ctx.message.content.split(' ')
        discord_id = ctx.author.id

        if len(args) == 1:

            try:
                username = DatabaseUtils.get_runner_from_discord_id(discord_id).speedrun_username
            except TypeError:
                await ctx.send(f'You currently have no speedrun.com account connected.\n'
                               f'To connect your account use `!connect [username]`')
                return

            await ctx.send(f'Account connected: `{username}`\n'
                           f'To change your connected account use `!connect [username]`')

        else:

            try:
                username = DatabaseUtils.get_runner_from_name(args[1]).speedrun_username
            except TypeError:
                await ctx.send('This account does not seem to have any individual level runs.\n'
                               'Please make sure you spelled it correctly.')
                return

            DatabaseUtils.add_discord_id_to_runner(discord_id, username)
            await ctx.send(f'Successfully connected account with username `{username}`.\n')
            print('Discord user', ctx.author.name, 'with id', discord_id, 'is now identified with speedrun.com username', username)


def setup(client):
    client.add_cog(ConnectCommand(client))
