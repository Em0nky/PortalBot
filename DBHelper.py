import sqlite3
from sqlite3 import Error

import pandas
import plotly.graph_objects as pgo
import plotly.io as pio
from PIL import Image

file = "PointsDB.db"
catList = ["Inbounds", "Out_of_Bounds", "Glitchless"]
chamberList = ["00_01", "02_03", "04_05", "06_07", "08", "09", "10",
               "11_12", "13", "14", "15", "16", "17", "18", "19", "e00", "e01", "e02",
               "Adv_13", "Adv_14", "Adv_15", "Adv_16", "Adv_17", "Adv_18"]


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


def export_leaderboard_image(board_length=10, category='Overall', level='Runner_Board'):
    """
    Translate database information into the pictures and other stuff
    if boardLength is -1, it's max
    """

    df = pandas.read_sql_query(f"SELECT * FROM {category.replace(' ', '_')}_{level};", get_connection())
    df = df.drop('SRCID', 1)
    if not level == 'Runner_Board':
        df = df.drop('SRCID', 1)
        df = df.drop('Category', 1)
        df = df.drop('Chamber', 1)
        df = df.drop('Date', 1)
        df = df.drop('Link', 1)
        df = df.drop('VideoLink', 1)
        df = df.drop('Ticks', 1)
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
    player = player.lower()

    df = pandas.read_sql_query(f"SELECT * FROM runs;", get_connection())
    df['RunnerNameLower'] = df['RunnerName'].str.lower()
    df = df[df['RunnerNameLower'] == player]
    if category is None:
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


def exportPlayerProfileDefaultDate(self, player):
    pio.kaleido.scope.default_scale = 2.0
    player = player.lower()

    df = pandas.read_sql_query(f"SELECT * FROM runs;", self.conn)
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


def leaderboardCommand(userMessage):
    """
    Command used for the bot to make overall points leaderboards
    Includes specification of category, length, and of both category and length
    """

    if len(userMessage) == 1:

        # !Leaderboard [NUMBER] creates specified length leaderboard
        if userMessage[0].isnumeric():  # numeric leaderboard requests(i.e. 15, 100)
            boardLength = int(userMessage[0])

            # If board length is less than 300 but more than 0
            if 300 > boardLength > 0:
                try:

                    # self.exportPointsLeaderboardImage(boardLength)
                    export_leaderboard_image(board_length=boardLength)
                    return f"Top {boardLength} Overall Players"

                except Error:
                    return "Error fetching data from database."
            else:
                return "Error: Invalid leaderboard length."

        else:  # Non-numeric leaderboard requests(i.e. max, inbounds, oob)
            # !Leaderboard max creates whole leaderboard
            if userMessage[0].lower() == "max":
                try:
                    export_leaderboard_image(board_length=-1)
                    return "All Players Overall"
                except Error:
                    return "Error fetching data from database."

            else:
                category = inputToCategory(userMessage[0])
                if category == '':
                    return "catfail"

                # self.exportCatPointsLeaderboardImageDefault(category)
                export_leaderboard_image(category=category)

                return f"Top {category} Players"

    # Leaderboard [CATEGORY] [NUMBER] creates a specific category leaderboard of specific length
    elif len(userMessage) == 2:
        try:

            category = inputToCategory(userMessage[0])

            boardLength = -1
            if not userMessage[1].lower() == "max":
                boardLength = int(userMessage[1])

            export_leaderboard_image(category=category, board_length=boardLength)
            # self.exportCatPointsLeaderboardImage(category, boardLength)
            return f"Top {boardLength if not boardLength == -1 else ''} {category} Players"

        except Error:
            return "Error fetching data from database."

    else:
        try:
            # !Leaderboard creates default length (10) leaderboard
            # self.exportPointsLeaderboardImageDefault()
            export_leaderboard_image()
            return f"Top Overall Players"

        except Error:
            return "Error fetching data from database."


def levelboardCommand(self, userMessage):
    """Command used for the bot to make level leaderboards
    Includes required specification of category and chamber"""

    category = userMessage[0].lower()
    level = userMessage[1]
    if len(userMessage) == 3:
        level = (userMessage[1] + userMessage[2]).replace(' ', '')

    category = self.inputToCategory(category)
    level = self.inputToChamber(level)

    if category == '':
        return "Error: Category not found."
    elif level == '':
        return "Error: Chamber not found."
    else:
        self.exportChamberPointsLeaderboardImage(category, level)
        replacement = '/'
        if level.lower().startswith('adv'):
            replacement = ' '
        return f"**{category} {level.replace('_', replacement)} Leaderboard:**"


def userprofileCommand(self, userMessage):
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

            nameID = self.exportPlayerProfileDefault(playerName)
            playerName = nameID[1]
            playerID = nameID[0]
            catRanks = ""
            missingCats = 0

            df = pandas.read_sql_query("SELECT * FROM Overall_Runner_Board;", self.conn)
            df.rename(columns={'SUM(Points)': 'Points'}, inplace=True)
            df = df.sort_values('Points', ascending=False)  # Sorts by Points
            df["Ranking"] = df["Points"].rank(method='min', ascending=False)
            df = df.round(decimals=2)
            df = df[df['RunnerName'] == playerName]  # Only Player Row
            oPlace = df['Ranking'].loc[df.index[0]]  # Gets Overall Place
            oPoints = df['Points'].loc[df.index[0]]  # Gets Overall Place

            for cat in self.catList:
                try:
                    df = pandas.read_sql_query(f"SELECT * FROM {cat}_Runner_Board;", self.conn)
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
                category = self.inputToCategory(category)

                nameID = self.exportPlayerProfileDefault(playerName)
                cat = category.replace(" ", "_")
                playerName = nameID[1]
                playerID = nameID[0]
                self.exportPlayerProfileCategory(playerName, cat)

                df = pandas.read_sql_query(f"SELECT * FROM {cat}_Runner_Board;", self.conn)
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
                category = self.inputToCategory(category)
                missingCats = 0

                if category == '':
                    return "Error: Invalid category"

                nameID = self.exportPlayerProfileDefault(playerName)
                playerName = nameID[1]
                playerID = nameID[0]

                self.exportPlayerProfileCategoryAll(playerName, category)

                df = pandas.read_sql_query(f"SELECT * FROM {category}_Runner_Board;", self.conn)
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

        except Error:
            return 'fail'


def inputToCategory(userCategory):
    """Takes input and converts it to correctly formatted category name"""

    userCategory = userCategory.lower()

    if userCategory == "inbob" or userCategory == "inbounds" or userCategory == "i":
        return "Inbounds"

    elif userCategory == "oob" or userCategory == "o":
        return "Out of Bounds"

    elif userCategory == "gless" or userCategory == "glitchless" or userCategory == "g":
        return "Glitchless"

    else:
        return ""


def inputToChamber(userChamber):
    """Takes input and converts it to correctly formatted chamber name"""
    userChamber = userChamber.replace('/', '')
    userChamber = userChamber.replace('-', '')

    if userChamber == '10':
        return chamberList[6]  # 10
    else:
        userChamber = userChamber.replace('0', '')

    if 'adv' in userChamber:
        userChamber = userChamber.replace('anced', '')

        if userChamber == 'adv13':
            return chamberList[18]  # adv13
        elif userChamber == 'adv14':
            return chamberList[19]  # adv14
        elif userChamber == 'adv15':
            return chamberList[20]  # adv15
        elif userChamber == 'adv16':
            return chamberList[21]  # adv16
        elif userChamber == 'adv17':
            return chamberList[22]  # adv17
        elif userChamber == 'adv18':
            return chamberList[23]  # adv18
        else:
            return ''

    elif 'e' in userChamber:
        if userChamber == 'e':
            return chamberList[15]  # e00
        elif userChamber == 'e1':
            return chamberList[16]  # e01
        elif userChamber == 'e2':
            return chamberList[17]  # e02
        else:
            return ''

    else:
        if userChamber == '' or userChamber == '1' or userChamber.lower() == "owo":
            return chamberList[0]  # 00-01
        elif userChamber == '23' or userChamber == '2' or userChamber == '3':
            return chamberList[1]  # 02-03
        elif userChamber == '45' or userChamber == '4' or userChamber == '5':
            return chamberList[2]  # 04-05
        elif userChamber == '67' or userChamber == '6' or userChamber == '7':
            return chamberList[3]  # 06-07
        elif userChamber == '8':
            return chamberList[4]  # 08
        elif userChamber == '9':
            return chamberList[5]  # 09
        elif userChamber == '1112' or userChamber == '11' or userChamber == '12':
            return chamberList[7]  # 11-12
        elif userChamber == '13':
            return chamberList[8]  # 13
        elif userChamber == '14':
            return chamberList[9]  # 14
        elif userChamber == '15':
            return chamberList[10]  # 15
        elif userChamber == '16':
            return chamberList[11]  # 16
        elif userChamber == '17':
            return chamberList[12]  # 17
        elif userChamber == '18':
            return chamberList[13]  # 18
        elif userChamber == '19':
            return chamberList[14]  # 19
        elif userChamber == '10':
            pass
        else:
            return ''
