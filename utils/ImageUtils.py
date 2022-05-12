import pandas
import plotly.graph_objects as pgo
import plotly.io as pio
from PIL import Image

import utils.DatabaseUtils as db

pio.kaleido.scope.default_scale = 2.0


class BoardSortValue:
    points_overall = 'points_overall'
    points_inbounds = 'points_inbounds'
    points_oob = 'points_oob'
    points_glitchless = 'points_glitchless'


def export_image_leaderboard(sort_value=BoardSortValue.points_overall,
                             sort_ascending=False, board_length=10):
    # Read SQL data into a pandas dataframe, sort it and get the first 'board_length' rows
    df = pandas.read_sql('select * from runners', db.get_connection())
    df = df.sort_values(sort_value, ascending=sort_ascending)
    df['rank_overall'] = df.apply(lambda row: '%d%s' % (
        row.rank_overall, {1: 'st', 2: 'nd', 3: 'rd'}.get(
            row.rank_overall if row.rank_overall < 20 else row.rank_overall % 10,
            'th')), axis=1)
    board_length = len(df) if (board_length == -1) else board_length
    df = df.head(board_length)

    header_mod = '🔼' if sort_ascending else '🔽'
    header_values = ['Place', 'Player', 'Overall', 'Glitchless', 'Inbounds',
                     'OoB']
    header_mod = '' if (
            sort_value is BoardSortValue.points_overall and sort_ascending is False) else header_mod

    match sort_value:
        case BoardSortValue.points_overall:
            header_values[2] = 'Overall' + header_mod
        case BoardSortValue.points_glitchless:
            header_values[3] = 'Glitch...' + header_mod
        case BoardSortValue.points_inbounds:
            header_values[4] = 'Inbo...' + header_mod
        case BoardSortValue.points_oob:
            header_values[5] = 'OoB' + header_mod

    # Generate table from dataframe using plotly
    fig = pgo.Figure(data=[pgo.Table(
        columnwidth=[15, 40, 20],
        header=dict(values=header_values,
                    height=22, line_color='black', fill_color='#1b1b1b',
                    font=dict(color='white', size=14, family='Consolas'),
                    align=['center', 'left', 'center']),
        cells=dict(
            values=[df.rank_overall, df.speedrun_username, df.points_overall,
                    df.points_glitchless, df.points_inbounds,
                    df.points_oob],
            line_color='black', fill_color='white',
            font=dict(color='black', size=14, family='Consolas'),
            align=['center', 'left', 'center']))
    ])

    mult_height = (20 * board_length) + 300
    pio.kaleido.scope.default_height = mult_height
    fig.write_image('list.png')

    # Crop the plotly image using pillow
    Image.open('list.png').crop(
        (160, 200, 1240, (mult_height * 2) - 355)).save('list.png')
    print('Generated new list.png')


def export_image_level(level, category, result_filter=None, board_length=10):
    # Modify Table height according to board length
    df = pandas.read_sql(
        'select * from runs where level="%s" and category="%s"%s' % (
            category, level,
            ' and %s' % result_filter.replace('&',
                                              ' and ') if result_filter is not None else ''),
        db.get_connection())

    df = df.sort_values('place', ascending=True)
    df['place'] = df.apply(
        lambda row: '%d%s' % (row.place, {1: 'st', 2: 'nd', 3: 'rd'}.get(
            row.place if row.place < 20 else row.place % 10, 'th')), axis=1)
    df['ticks'] = df.apply(
        lambda row: row.time / 15 if row.time / 15 % 1 == 0 else round(
            row.time / 15), axis=1)
    df = df.head(board_length)
    board_length = len(df)

    # Using plotly to generate table and subsequent image
    fig = pgo.Figure(data=[pgo.Table(
        columnwidth=[15, 60, 20, 25, 20],
        header=dict(values=['Place', 'Player', 'Points', 'Time', 'Ticks'],
                    height=22,
                    line_color='black',
                    fill_color='#1b1b1b',
                    font=dict(color='white', size=14, family='Consolas'),
                    align=['center', 'left', 'center']),
        cells=dict(
            values=[df.place, df.speedrun_username, df.points, df.time / 1000,
                    df['ticks']],
            line_color='black',
            fill_color='white',
            font=dict(color='black', size=14, family='Consolas'),
            align=['center', 'left', 'center']))
    ])

    # Modify Table height according to board length
    mult_height = (20 * board_length) + 300
    pio.kaleido.scope.default_height = mult_height
    fig.write_image("list.png")

    # Crop the plotly image
    Image.open("list.png").crop(
        (160, 200, 1240, (mult_height * 2) - 355)).save("list.png")
    print('Generated new list.png')


def export_image_profile(player):

    df = pandas.read_sql_query(
        f'select * from runs where speedrun_username="%s"' % player,
        db.get_connection())
    df = df.sort_values('points', ascending=False)
    df['ticks'] = df.apply(
        lambda row: row.time / 15 if row.time / 15 % 1 == 0 else round(
            row.time / 15), axis=1)
    board_length = len(df) if len(df) <= 10 else 10
    df = df.head(board_length)

    # Using plotly to generate table and subsequent image
    fig = pgo.Figure(data=[pgo.Table(
        columnwidth=[25, 25, 15, 15, 25, 20],
        header=dict(values=['Category', 'Chamber', 'Place', 'Points', 'Time', 'Ticks'],
                    height=22,
                    line_color='black',
                    fill_color='#1b1b1b',
                    font=dict(color='white', size=14, family='Consolas'),
                    align='center'),
        cells=dict(
            values=[df.category, df.level, df.place, df.points, df.time / 1000,
                    df.ticks],
            line_color='black',
            fill_color='white',
            font=dict(color='black', size=14, family='Consolas'),
            align='center'))
    ])

    mult_height = (20 * board_length) + 300
    pio.kaleido.scope.default_height = mult_height
    fig.write_image('list.png')

    # Cropping the plotly image
    Image.open('list.png').crop((160, 200, 1240, (mult_height * 2) - 355))\
        .save('list.png')
