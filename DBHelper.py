import sqlite3
from sqlite3 import Error

import pandas
import plotly.graph_objects as pgo
import plotly.io as pio
from PIL import Image

from utils import ImageUtils, BotUtils

file = "PointsDB.db"


def get_connection():
    """
    Gets connection to the database
    """

    conn = None
    try:
        conn = sqlite3.connect(file)
    except Error as e:
        print(e)
    return conn


def leaderboard_max_length(category='Overall', level='Runner_Board'):

    df = pandas.read_sql_query(f"SELECT * FROM {category.replace(' ', '_')}_{level};", get_connection())
    return len(df)


def exportPlayerProfileDefault(player):

    pio.kaleido.scope.default_scale = 2.0
    player = player.lower()

    df = pandas.read_sql_query(f"SELECT * FROM runs;", get_connection())
    df['RunnerNameLower'] = df['RunnerName'].str.lower()
    df = df[df['RunnerNameLower'] == player]
    playerID = df['SRCID'].loc[df.index[0]]
    playerName = df['RunnerName'].loc[df.index[0]]
    df = df.drop('RunnerNameLower', 1)
    df = df.drop('RunnerName', 1)
    df = df.drop('SRCID', 1)
    df = df.drop('Link', 1)
    df = df.drop('VideoLink', 1)
    df = df.drop('Date', 1)
    df.drop('Ticks', 1)

    return [playerID, playerName]


def exportPlayerProfileCategory(self, player, category):
    pio.kaleido.scope.default_scale = 2.0
    pio.kaleido.scope.default_height = 430  # Table Height

    player = player.lower()

    df = pandas.read_sql_query(f"SELECT * FROM runs;", self.conn)
    df['RunnerNameLower'] = df['RunnerName'].str.lower()
    df = df[df['RunnerNameLower'] == player]
    df = df[df['Category'] == category]
    playerID = df['SRCID'].loc[df.index[0]]
    playerName = df['RunnerName'].loc[df.index[0]]
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
    df = df.nsmallest(10, 'Place')  # Top 5 Runs
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
    return [playerID, playerName]


def exportPlayerProfileCategoryAll(self, player, category):
    pio.kaleido.scope.default_scale = 2.0

    player = player.lower()

    df = pandas.read_sql_query(f"SELECT * FROM runs;", self.conn)
    df['RunnerNameLower'] = df['RunnerName'].str.lower()
    df = df[df['RunnerNameLower'] == player]
    df = df[df['Category'] == category]
    playerID = df['SRCID'].loc[df.index[0]]
    playerName = df['RunnerName'].loc[df.index[0]]
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

    boardLength = int(df.size / 5)
    heightMult = (20 * boardLength) + 300

    pio.kaleido.scope.default_height = heightMult  # Table Height

    # Sorts by Chamber Order
    advQuery = df.query('Chamber.str.startswith("Adv")')
    advQuery = advQuery.sort_values('Chamber')
    escQuery = df.query('Chamber.str.startswith("e")')
    escQuery = escQuery.sort_values('Chamber')
    numQuery = df.query('Chamber.str.startswith("1") or Chamber.str.startswith("0")')
    numQuery = numQuery.sort_values('Chamber')

    df = pandas.concat([numQuery, escQuery, advQuery])
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
    return [playerID, playerName]


def exportPlayerProfileDefaultDate(player):
    pio.kaleido.scope.default_scale = 2.0
    player = player.lower()

    df = pandas.read_sql_query(f"SELECT * FROM runs;", get_connection())
    df['RunnerNameLower'] = df['RunnerName'].str.lower()
    df = df[df['RunnerNameLower'] == player]
    playerName = df['RunnerName'].loc[df.index[0]]
    df['Date'] = df['Date'].str.replace("_", "-")
    df['Date'] = pandas.to_datetime(df['Date'], format='%Y-%m-%d')
    df = df.sort_values(by='Date', ascending=False)
    df = df.drop('RunnerNameLower', 1)
    df = df.drop('RunnerName', 1)
    df = df.drop('SRCID', 1)
    df = df.drop('Link', 1)
    df = df.drop('VideoLink', 1)
    df = df.drop('Ticks', 1)
    df['Chamber'] = df['Chamber'].str.replace("_", " ")
    df['Category'] = df['Category'].str.replace("_", " ")
    df = df.head(10)  # Recent 10 Runs

    df.Points = df.Points.round(decimals=2)
    df.Time = df.Time.round(decimals=3)
    df['Ticks'] = df.apply(lambda row: row.Time / .015, axis=1)
    df.Ticks = df.Ticks.round(decimals=0)
    columnHeaders = ['Category', 'Chamber', 'Place', 'Points', 'Time', 'Ticks', 'Date']

    # Using plotly to generate table and subsequent image
    fig = pgo.Figure(data=[pgo.Table(
        columnorder=[0, 1, 2, 3, 4, 5, 6],
        columnwidth=[25, 20, 15, 15, 15, 15, 20],
        header=dict(values=list(columnHeaders),
                    fill_color='#1b1b1b',
                    font=dict(color='white', size=12),
                    align='left'),
        cells=dict(values=[df.Category, df.Chamber, df.Place, df.Points, df.Time, df.Ticks, df.Date],
                   fill_color='#D3D3D3',
                   align='left'))
    ])
    boardLength = len(df)
    heightMult = (20 * boardLength) + 300
    pio.kaleido.scope.default_height = heightMult
    fig.write_image("list.png")

    # Cropping the plotly image
    listimg = Image.open("list.png")
    listimg = listimg.crop((160, 200, 1227, (heightMult * 2) - 345))
    listimg.save("list.png")
    return [playerName]


def exportPlayerProfileCategoryDate(self, player, category):
    pio.kaleido.scope.default_scale = 2.0
    player = player.lower()

    df = pandas.read_sql_query(f"SELECT * FROM runs;", self.conn)
    df['RunnerNameLower'] = df['RunnerName'].str.lower()
    df = df[df['RunnerNameLower'] == player]
    df = df[df['Category'] == category]
    playerName = df['RunnerName'].loc[df.index[0]]
    df['Date'] = df['Date'].str.replace("_", "-")
    df['Date'] = pandas.to_datetime(df['Date'], format='%Y-%m-%d')
    df = df.sort_values(by='Date', ascending=False)
    df = df.drop('RunnerNameLower', 1)
    df = df.drop('RunnerName', 1)
    df = df.drop('SRCID', 1)
    df = df.drop('Link', 1)
    df = df.drop('VideoLink', 1)
    df = df.drop('Ticks', 1)
    df['Chamber'] = df['Chamber'].str.replace("_", " ")
    df['Category'] = df['Category'].str.replace("_", " ")
    df = df.head(10)  # Recent 10 Runs

    df.Points = df.Points.round(decimals=2)
    df.Time = df.Time.round(decimals=3)
    df['Ticks'] = df.apply(lambda row: row.Time / .015, axis=1)
    df.Ticks = df.Ticks.round(decimals=0)
    columnHeaders = ['Category', 'Chamber', 'Place', 'Points', 'Time', 'Ticks', 'Date']

    # Using plotly to generate table and subsequent image
    fig = pgo.Figure(data=[pgo.Table(
        columnorder=[0, 1, 2, 3, 4, 5, 6],
        columnwidth=[25, 20, 15, 15, 15, 15, 20],
        header=dict(values=list(columnHeaders),
                    fill_color='#1b1b1b',
                    font=dict(color='white', size=12),
                    align='left'),
        cells=dict(values=[df.Category, df.Chamber, df.Place, df.Points, df.Time, df.Ticks, df.Date],
                   fill_color='#D3D3D3',
                   align='left'))
    ])
    boardLength = len(df)
    heightMult = (20 * boardLength) + 300
    pio.kaleido.scope.default_height = heightMult
    fig.write_image("list.png")

    # Cropping the plotly image
    listimg = Image.open("list.png")
    listimg = listimg.crop((160, 200, 1227, (heightMult * 2) - 345))
    listimg.save("list.png")
    return [playerName]


def userprofileCommand(userMessage):
    """Command used for the bot to make a user profile
    !Profile
    Potentially to be added with database to link discord profile with src
    !Profile [PLAYER]
    Includes user's top 5 runs, overall place w/ total points, and place w/ points for each cat
    !Profile [PLAYER] [CATEGORY]
    or top 10 runs of a specific cat and points
    !Profile [PLAYER] [CATEGORY] ALL
    or all runs from a specific cat."""

    # Return: (PLAYER's Profile:), (OVERALL POINTS),
    # CAT1 POINTS, CAT1 Place...
    # Overall Place
    # Export Top10 Runs

    # Return: (PLAYER's CATEGORY Profile:),
    # CATEGORY POINTS, CATEGORY PLACE
    # Export Top 10 Runs OR All

    # !Profile [PLAYER]
    # Returns - userMessage, [Oplace, Opoints, cat1, place1, points1...], playerID, playerName

    try:
        if len(userMessage) == 1:
            playerName = str(userMessage[0])

            nameID = exportPlayerProfileDefault(playerName)
            # nameID = export_profile_image(playerName)
            playerName = nameID[1]
            playerID = nameID[0]
            catRanks = ""
            missingCats = 0

            df = pandas.read_sql_query("SELECT * FROM Overall_Runner_Board;", get_connection())
            df.rename(columns={'SUM(Points)': 'Points'}, inplace=True)
            df = df.sort_values('Points', ascending=False)  # Sorts by Points
            df["Ranking"] = df["Points"].rank(method='min', ascending=False)
            df = df.round(decimals=2)
            df = df[df['RunnerName'] == playerName]  # Only Player Row
            oPlace = df['Ranking'].loc[df.index[0]]  # Gets Overall Place
            oPoints = df['Points'].loc[df.index[0]]  # Gets Overall Place

            for cat in BotUtils.category_list:
                try:
                    df = pandas.read_sql_query(f"SELECT * FROM {cat}_Runner_Board;", get_connection())
                    df.rename(columns={'SUM(Points)': 'Points'}, inplace=True)
                    df = df.sort_values('Points', ascending=False)  # Sorts by Points
                    df["Ranking"] = df["Points"].rank(method='min', ascending=False)
                    df = df.round(decimals=2)
                    df = df[df['RunnerName'] == playerName]  # Only Player Row
                    # TODO if df what do you mean by this?? ^lun
                    cPlace = (df['Ranking'].loc[df.index[0]])  # Gets Cat Place
                    cPoints = (df['Points'].loc[df.index[0]])  # Gets Cat Place
                    cat = cat.replace("_", " ")
                    catRanks = catRanks + f',{cat},{cPlace:.0f},{cPoints:.2f}'

                except:
                    missingCats += 1
                    print(f"Player Doesn't have {cat} ILs")

            if missingCats >= 3:
                return "Error: Invalid Category"

            returnArray = [str(f'{oPlace:.0f},{oPoints:.2f}'), str(catRanks), playerID, playerName]
            return returnArray

        elif len(userMessage) == 2:
            try:

                playerName = str(userMessage[0])
                category = str(userMessage[1])
                category = BotUtils.inputToCategory(category)

                nameID = exportPlayerProfileDefault(playerName)
                # nameID = export_profile_image(playerName)
                cat = category.replace(" ", "_")
                playerName = nameID[1]
                playerID = nameID[0]
                exportPlayerProfileCategory(playerName, cat)
                # export_profile_image(playerName, category=cat)

                df = pandas.read_sql_query(f"SELECT * FROM {cat}_Runner_Board;", get_connection())
                df.rename(columns={'SUM(Points)': 'Points'}, inplace=True)
                df = df.sort_values('Points', ascending=False)  # Sorts by Points
                df = df.round(decimals=2)
                df["Ranking"] = df["Points"].rank(method='min', ascending=False)
                df = df[df['RunnerName'] == playerName]  # Only Player Row
                cPlace = df['Ranking'].loc[df.index[0]]  # Gets Cat Place
                cPoints = df['Points'].loc[df.index[0]]  # Gets Cat Place
                category = category.replace("_", " ")

                returnArray = [str(f',{category},{cPlace:.0f},{cPoints:.2f}'), playerID, playerName]
                print(returnArray)
                return returnArray

            except Error:
                return 'Error fetching data from database.'

        elif len(userMessage) == 3:
            try:
                playerName = str(userMessage[0])
                category = str(userMessage[1])
                category = BotUtils.inputToCategory(category)

                if category == '':
                    return "Error: Invalid category"

                nameID = exportPlayerProfileDefault(playerName)
                # nameID = export_profile_image(playerName)
                playerName = nameID[1]
                playerID = nameID[0]

                exportPlayerProfileCategoryAll(playerName, category)
                # export_profile_image(playerName, board_length=-1, category=category)

                df = pandas.read_sql_query(f"SELECT * FROM {category}_Runner_Board;", get_connection())
                df.rename(columns={'SUM(Points)': 'Points'}, inplace=True)
                df = df.sort_values('Points', ascending=False)  # Sorts by Points
                df = df.round(decimals=2)
                df["Ranking"] = df["Points"].rank(method='min', ascending=False)
                df = df[df['RunnerName'] == playerName]  # Only Player Row
                cPlace = df['Ranking'].loc[df.index[0]]  # Gets Cat Place
                cPoints = df['Points'].loc[df.index[0]]  # Gets Cat Place

                returnArray = [str(f',{category},{cPlace:.0f},{cPoints:.2f}'), playerID, playerName]
                print(returnArray)
                return returnArray

            except Error:
                return 'Error fetching data from database.'

    except:
        return 'Error fetching data from speedrun.com'


def runCommand(self, userMessage):
    """Command used for the bot to return information on a run
    !Run [PLAYER] [CATEGORY] [CHAMBER]"""

    print(userMessage)

    level = userMessage[2]

    if len(userMessage) == 4:
        level = (userMessage[2] + userMessage[3]).replace(' ', '')

    player = userMessage[0]
    category = self.inputToCategory(userMessage[1])
    level = self.inputToChamber(level)

    print(category)

    try:

        undLevel = level.replace(' ', '_')
        undCategory = category.replace(' ', '_')
        df = pandas.read_sql_query(f"SELECT * FROM {undCategory}_{undLevel};", self.conn)

        df['RunnerNameLower'] = df['RunnerName'].str.lower()
        df = df[df['RunnerNameLower'] == player.lower()]
        playerName = df['RunnerName'].loc[df.index[0]]

        # still need to fix 14
        runValues = df.loc[df['RunnerName'] == playerName].values[0]

        player = runValues[3]
        runPlace = runValues[2]
        runPoints = runValues[7]
        runTime = runValues[5]
        runLink = runValues[9]
        runVid = runValues[10]
        runDate = runValues[8].replace('_', '-')
        playerID = runValues[4]
        runValues = [player, category, level, runPlace, runPoints, runTime, runLink, runVid, runDate, playerID]

        print(f'debug', runValues)
        return runValues

    except Error:
        return "Error fetching data from database."
    except IndexError:
        return f'Error: {player} does not have an IL run in {category} {level}'


def recentCommand(self, userMessage):
    """Command used for the bot to make a list of recent runs
    !recent
    Potentially to be added with database to link discord profile with src
    !recent [PLAYER]
    Overall recent runs
    !recent [PLAYER] [CATEGORY]
    Category recent runs
    """

    if len(userMessage) == 0:
        # Not Implemented
        pass

    elif len(userMessage) == 1:
        # !Recent [PLAYER]
        try:
            player = userMessage[0]
            playerName = self.exportPlayerProfileDefaultDate(player)
            return playerName

        except Error:
            return 'fail'

    elif len(userMessage) == 2:
        # !Recent [PLAYER] [CATEGORY]
        try:

            player = userMessage[0]
            category = self.inputToCategory(userMessage[1])

            if category == '':
                return "catfail"

            playerName = self.exportPlayerProfileCategoryDate(player, category)
            playerName = playerName[0]
            return [playerName, category]
        except:
            print('balls')
