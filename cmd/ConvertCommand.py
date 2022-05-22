import math
import re
from discord.ext import commands


# Pretty print milliseconds into a time format
def human_time(millis: int) -> str:
    seconds, millis = divmod(millis, 1000)
    minutes, seconds = divmod(seconds, 60)
    return f'{minutes:02d}:{seconds:02d}.{millis:03d}'


def convert_ms_to_ticks(millis: int) -> int:
    return round(millis / 15)


def convert_ticks_to_ms(ticks: int) -> int:
    return ticks * 15


class ConvertCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['conv', 'ticks', 'time'])
    async def convert(self, ctx):

        args = ctx.message.content.split(' ')

        if len(args) == 1:
            await ctx.send('Please enter a time or ticks, example: `!convert 2300` or `!convert 34.500`')
            return

        time = args[1]

        # If time is numeric, we treat is as ticks and convert to human time
        if time.isnumeric():

            ms = convert_ticks_to_ms(int(time))
            await ctx.send(f'Converted time: `{human_time(ms)}`')

        else:

            # If time matches ss.mmm
            if re.match(r'^[1-5]?\d\.\d+$', time):
                ms = (int(time.split('.')[0]) * 1000) + int(time.split(".")[1])

                if ms % 15 != 0:
                    ticks = round(ms / 15) if (ms / 15) % 1 < .5 else math.ceil(ms / 15)
                    await ctx.send(f'Converted ticks: `{round(ms / 15)}*` | Did you mean `{human_time(ticks*15)}`?')
                else:
                    ticks = convert_ms_to_ticks(ms)
                    await ctx.send(f'Converted ticks: `{ticks}`')

            # If time matches MM:ss.mmm
            elif re.match(r"^[0-5]?\d+:[0-5]?\d\.\d{3}$", time):

                ms = (int(time.split(':')[0]) * 60000) + \
                     (int(time.split(':')[1].split('.')[0]) * 1000) + \
                     int(time.split('.')[1])

                if ms % 15 != 0:
                    ticks = math.floor(ms / 15) if (ms / 15) % 1 < .5 else math.ceil(ms / 15)
                    await ctx.send(f'Converted ticks: `{round(ms / 15)}*` | Did you mean `{human_time(ticks*15)}`?')
                else:
                    ticks = convert_ms_to_ticks(ms)
                    await ctx.send(f'Converted ticks: `{ticks}`')

            # If time doesn't match anything
            else:
                await ctx.send('Invalid argument. Please use ticks or a proper time format.')


def setup(client):
    client.add_cog(ConvertCommand(client))
