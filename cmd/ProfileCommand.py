from discord.ext import commands


class ProfileCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def profile(self, ctx):
        pass


def setup(client):
    client.add_cog(ProfileCommand(client))
