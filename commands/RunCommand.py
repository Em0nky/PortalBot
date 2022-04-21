import DBHelper
from utils import BotUtils


async def on_command(event, args):

    if len(args) < 3:
        await event.channel.send('Missing arguments: `!help run`')
        return

    if len(args) >= 3:

        runInfo = DBHelper.runCommand(args)

        if len(runInfo) == 10:
            embed = BotUtils.embedRun(runInfo)
            await event.channel.send(embed=embed)
        else:
            await event.channel.send(runInfo)
