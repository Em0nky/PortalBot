from discord.ext import commands


class RunCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def run(self, ctx):
        args = ctx.message.content.split(' ')

        if len(args) < 3:
            await ctx.send('Missing arguments: `!help run`')




def setup(client):
    client.add_cog(RunCommand(client))
