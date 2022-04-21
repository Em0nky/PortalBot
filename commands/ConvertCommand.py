from utils import BotUtils


async def on_command(event, args):

    if not len(args) == 1:
        await event.channel.send('Error: Not enough arguments: `!help convert`')
        return

    if not args[0].isnumeric():
        try:

            ticks = BotUtils.convert_to_ticks(args[0])

            if not (ticks % 1) == 0:
                newTicks = ticks
                ticks = str(int(ticks)) + '*'

                if (newTicks % 1) < .4:
                    newTicks = int(newTicks)
                elif (newTicks % 1) > .4:
                    newTicks = int(newTicks + 1)
                await event.channel.send(f'Converted ticks `{ticks}` | Did you mean `{BotUtils.convert_to_human_time(newTicks)}` instead?')

            else:
                ticks = int(ticks)
                await event.channel.send(f'Converted ticks `{ticks}`')

        except ValueError:
            await event.channel.send('Invalid time format given.')

    else:
        time = BotUtils.convert_to_human_time(args[0])
        await event.channel.send(f'Converted time `{time}`')
