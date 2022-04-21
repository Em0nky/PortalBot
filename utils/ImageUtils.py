import pandas
import plotly.graph_objects as pgo
import plotly.io as pio
from PIL import Image

import DBHelper


def export_leaderboard_image(board_length=10, category='Overall', level='Runner_Board'):
    """
    Translate database information into the pictures and other stuff
    If boardLength is -1, it's max
    """

    df = pandas.read_sql_query(f"SELECT * FROM {category.replace(' ', '_')}_{level};", DBHelper.get_connection())
    df = df.drop('SRCID', 1)

    if not level == 'Runner_Board':

        df = df.drop('Date', 1)
        df = df.drop('Link', 1)
        df = df.drop('VideoLink', 1)

    df.rename(columns={'SUM(Points)': 'Points'}, inplace=True)
    df.rename(columns={'RunnerName': 'Player'}, inplace=True)
    df = df.sort_values('Points', ascending=False)
    df = df.round(decimals=2)
    df["Ranking"] = df["Points"].rank(method='min', ascending=False)

    if board_length == -1:
        board_length = len(df)
    df = df.nsmallest(board_length, 'Ranking')

    table_columns = [2, 3, 1]
    table_width = [50, 40, 25]
    table_header = list(df.columns)
    table_cells = [df.Player, df.Points, df.Ranking]

    if not level == 'Runner_Board':
        table_columns = [1, 2, 3, 4, 5]
        table_width = [25, 60, 40, 40, 40]
        table_header = list(['Place', 'Player', 'Points', 'Time', 'Ticks'])
        table_cells = [df.Place, df.Player, df.Points, df.Time, df.Ticks]

    # Using plotly to generate table and subsequent image
    fig = pgo.Figure(data=[pgo.Table(
        columnorder=table_columns,
        columnwidth=table_width,
        header=dict(values=table_header,
                    fill_color='#1b1b1b',
                    font=dict(color='white', size=12),
                    align='left'),
        cells=dict(values=table_cells,
                   fill_color='#D3D3D3',
                   align='left'))
    ])

    # Modifies Table height according to board length

    heightMult = (20 * board_length) + 300
    pio.kaleido.scope.default_scale = 2.0
    pio.kaleido.scope.default_height = heightMult
    fig.write_image("list.png")

    # Cropping the plotly image
    listimg = Image.open("list.png")
    listimg = listimg.crop((160, 200, 1240, (heightMult * 2) - 345))
    listimg.save("list.png")


def export_profile_image(player, board_length=10, category=None):

    pio.kaleido.scope.default_scale = 2.0

    df = pandas.read_sql_query(f"SELECT * FROM runs;", DBHelper.get_connection())
    df['RunnerNameLower'] = df['RunnerName'].str.lower()
    df = df[df['RunnerNameLower'] == player.lower()]

    if category is None:
        df = df[df['Category'] == category]

    df = df.drop('RunnerNameLower', 1)
    df = df.drop('RunnerName', 1)
    df = df.drop('SRCID', 1)
    df = df.drop('Link', 1)
    df = df.drop('VideoLink', 1)
    df = df.drop('Date', 1)
    df = df.drop('Ticks', 1)
    df['Chamber'] = df['Chamber'].str.replace("_", " ")
    df['Category'] = df['Category'].str.replace("_", " ")

    df = df.sort_values('Points', ascending=False)
    df.Points = df.Points.round(decimals=2)
    df.Time = df.Time.round(decimals=3)
    df['Ticks'] = df.apply(lambda row: row.Time / .015, axis=1)
    df.Ticks = df.Ticks.round(decimals=0)

    if board_length == -1:
        board_length = len(df)

    df = df.nsmallest(board_length, 'Place')  # Top 5 Runs
    columnHeaders = ['Category', 'Chamber', 'Place', 'Points', 'Time', 'Ticks']

    # Using plotly to generate table and subsequent image
    fig = pgo.Figure(data=[pgo.Table(
        columnorder=[0, 1, 2, 3, 4, 5],
        columnwidth=[25, 25, 15, 15, 25, 20],
        header=dict(values=list(columnHeaders),
                    fill_color='#1b1b1b',
                    font=dict(color='white', size=12),
                    align='left'),
        cells=dict(values=[df.Category, df.Chamber, df.Place, df.Points, df.Time, df.Ticks],
                   fill_color='#D3D3D3',
                   align='left'))
    ])

    boardLength = len(df)
    heightMult = (20 * boardLength) + 300
    pio.kaleido.scope.default_height = heightMult
    fig.write_image("list.png")

    # Cropping the plotly image
    listimg = Image.open("list.png")
    listimg = listimg.crop((160, 200, 1240, (heightMult * 2) - 345))
    listimg.save("list.png")
