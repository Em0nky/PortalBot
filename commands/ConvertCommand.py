from utils import BotUtils


async def on_command(event, args):

    if len(args) == 1:
        if not args[0].isnumeric():
            try:

                ticks = BotUtils.convert_to_ticks(args[0])

                if not ((ticks * 15) % 15) == 0:
                    ticks = str(int(ticks)) + '*'
                else:
                    ticks = int(ticks)
                await event.channel.send('Converted ticks `' + str(ticks) + "`")

            except ValueError:
                await event.channel.send('Invalid time format given.')

        else:
            time = BotUtils.convert_to_human_time(args[0])
            await event.channel.send('Converted time `' + str(time) + '`')
