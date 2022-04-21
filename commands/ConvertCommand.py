from utils import BotUtils


async def on_command(event, args):

    if len(args) == 1:
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
                    await event.channel.send(f'Converted ticks `{str(ticks)}` | Did you mean `{BotUtils.convert_to_human_time(newTicks)}` instead?')

                else:
                    ticks = int(ticks)
                    await event.channel.send(f'Converted ticks `{str(ticks)}`')

            except ValueError:
                await event.channel.send(f'Invalid time format given.')

        else:
            time = BotUtils.convert_to_human_time(args[0])
            await event.channel.send(f'Converted time `{str(time)}`')
