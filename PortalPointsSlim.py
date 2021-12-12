from discord import user
import srcomapi, srcomapi.datatypes as dt, pandas as pd
import plotly.graph_objects as pgo, plotly.io as pio
from PIL import Image

api = srcomapi.SpeedrunCom(); api.debug = 1


class PortalPoints:
    """
    Class for accessing SRC api in order to assign points to IL placements
    as well as functions for bot commands
    """

    def __init__(self):
        """
        Constructor, grabs api stuff and creates 
        catList, chamberList, chamberListNoAdv, chamberListOnlyAdv, and fullLeaderboard
        
        """
        
        #Grabbing Information from SRC
        apiSuccessGrab = False
        while(apiSuccessGrab == False):
            try: 
                apiSuccessGrab = True
                #api stuff
                game = api.search(srcomapi.datatypes.Game, {"name": "Portal"})[0]

                #Grabbing API stuff and assigning into portal runs dict
                self.portal_runs = {}
                for category in game.categories:
                    if not category.name in self.portal_runs:
                        self.portal_runs[category.name] = {}
                    if category.type == 'per-level':
                        for level in game.levels:
                            self.portal_runs[category.name][level.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/level/{}/{}?embed=variables".format(game.id, level.id, category.id)))
            except:
                #api failed to grab stuff
                apiSuccessGrab = False
                print("Something went wrong with the API stuff!")
        
        #Lists
        #Categories
        self.catList = ["Inbounds", "Out of Bounds", "Glitchless"]

        #All Chambers
        self.chamberList = ["00-01", "02-03", "04-05", "06-07", "08", "09", "10", 
            "11-12", "13", "14", "15", "16", "17", "18", "19", "e00", "e01", "e02",
            "Adv 13", "Adv 14", "Adv 15", "Adv 16", "Adv 17", "Adv 18"]

        #Only Normal Chambers
        self.chamberListNoAdv = ["00-01", "02-03", "04-05", "06-07", "08", "09", "10", 
            "11-12", "13", "14", "15", "16", "17", "18", "19", "e00", "e01", "e02"]
            
        #Adv Chambers
        self.chamberListOnlyAdv = ["Adv 13", "Adv 14", "Adv 15", "Adv 16", "Adv 17", "Adv 18"]

        #LeaderboardText?
        self.fullLeaderboard = ""

    #List of runs creators
    def createInboundsList(self):
        """Returns a 2D list of every inbounds IL run
        List Format: CATEGORY, CHAMBER, PLAYER, PLACE, POINTS, TIME"""

        inboundsList = []
        
        for currentChamber in self.chamberList:
            currentList = []
            placeCounter = 0
            #runPlace, runTime, playerName, runPoints
            while placeCounter < (len(self.portal_runs["Inbounds"][currentChamber].runs)):
                currentRun = self.portal_runs["Inbounds"][currentChamber].runs[placeCounter]["run"].data
                runPlace = (self.portal_runs["Inbounds"][currentChamber].runs[placeCounter]["place"]) #Gets Player Place
                runTime = currentRun["times"]["primary_t"] #Gets Player Time
                playerName = ((self.portal_runs["Inbounds"][currentChamber].runs[placeCounter]["run"].players)[0].name) #Gets Player Name
                runPoints = (((50 - (runPlace - 1))**2) / 50) #Calculates Point Value

                currentList = ["Inbounds", currentChamber, playerName, runPlace, runPoints, runTime] #creates single run entry list

                inboundsList.append(currentList) #Adds that run to the full list
                placeCounter += 1

        return inboundsList

    def createOobList(self):
        """Returns a 2D list of every oob IL run
        List Format: CATEGORY, CHAMBER, PLAYER, PLACE, POINTS, TIME"""

        oobList = []
        
        for currentChamber in self.chamberList:
            currentList = []
            placeCounter = 0
            #runPlace, runTime, playerName, runPoints
            while placeCounter < (len(self.portal_runs["Out of Bounds"][currentChamber].runs)):
                currentRun = self.portal_runs["Out of Bounds"][currentChamber].runs[placeCounter]["run"].data
                runPlace = (self.portal_runs["Out of Bounds"][currentChamber].runs[placeCounter]["place"])
                runTime = currentRun["times"]["primary_t"] #Gets Player Time
                playerName = ((self.portal_runs["Out of Bounds"][currentChamber].runs[placeCounter]["run"].players)[0].name) #Gets Player Name
                runPoints = (((50 - (runPlace - 1))**2) / 50) #Calculates Point Value

                currentList = ["Out of Bounds", currentChamber, playerName, runPlace, runPoints, runTime] #creates single run entry list

                oobList.append(currentList) #Adds that run to the full list
                placeCounter += 1

        return oobList

    def createGlessList(self):
        """Returns a 2D list of every glitchless IL run
        List Format: CATEGORY, CHAMBER, PLAYER, PLACE, POINTS, TIME"""

        glessList = []
        
        for currentChamber in self.chamberList:
            currentList = []
            placeCounter = 0
            #runPlace, runTime, playerName, runPoints
            while placeCounter < (len(self.portal_runs["Glitchless"][currentChamber].runs)):
                currentRun = self.portal_runs["Glitchless"][currentChamber].runs[placeCounter]["run"].data
                runPlace = (self.portal_runs["Glitchless"][currentChamber].runs[placeCounter]["place"])
                runTime = currentRun["times"]["primary_t"] #Gets Player Time
                playerName = ((self.portal_runs["Glitchless"][currentChamber].runs[placeCounter]["run"].players)[0].name) #Gets Player Name
                runPoints = (((50 - (runPlace - 1))**2) / 50) #Calculates Point Value

                currentList = ["Glitchless", currentChamber, playerName, runPlace, runPoints, runTime] #creates single run entry list

                glessList.append(currentList) #Adds that run to the full list
                placeCounter += 1

        return glessList

    def createSpecificChamberListBetter(self, chosenCat, chosenChamber):
        """Returns a 2D list of runs for a specific chamber of a specific category using arguments
        List Format: CATEGORY, CHAMBER, PLAYER, PLACE, POINTS, TIME"""

        customList = []
        currentList = []
        
        placeCounter = 0

        #runPlace, runTime, playerName, runPoints
        while placeCounter < (len(self.portal_runs[chosenCat][chosenChamber].runs)):
            currentRun = self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].data
            runPlace = (self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["place"]) #Gets Player Place
            runTime = currentRun["times"]["primary_t"] #Gets Player Time
            playerName = ((self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].players)[0].name) #Gets Player Name
            runPoints = (((50 - (runPlace - 1))**2) / 50) #Calculates Point Value

            currentList = [chosenCat, chosenChamber, playerName, runPlace, runPoints, runTime] #creates single run entry list

            customList.append(currentList) #Adds that run to the full list
            placeCounter += 1

        return customList

    def createSpecificChamberListBot(self, chosenCat, chosenChamber):
        """Returns a 2D list of runs for a specific chamber of a specific category using arguments
        List Format: CATEGORY, CHAMBER, PLAYER, PLACE, POINTS, TIME"""

        customList = []
        currentList = []
        
        placeCounter = 0

        #runPlace, runTime, playerName, runPoints
        while placeCounter < (len(self.portal_runs[chosenCat][chosenChamber].runs)):
            currentRun = self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].data
            runPlace = (self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["place"]) #Gets Player Place
            runTime = currentRun["times"]["primary_t"] #Gets Player Time
            playerName = ((self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].players)[0].name) #Gets Player Name
            #runTicks = (self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].ticks) #Gets Run Ticks?
            runPoints = (((50 - (runPlace - 1))**2) / 50) #Calculates Point Value

            currentList = [runPlace, playerName, runPoints, runTime] #creates single run entry list
            
            customList.append(currentList) #Adds that run to the full list
            placeCounter += 1

        return customList


    def createSpecificChamberListMore(self, chosenCat, chosenChamber):
        """Returns a 2D list of runs for a specific chamber of a specific category using arguments
        List Format: CATEGORY, CHAMBER, PLAYER, PLACE, POINTS, TIME"""

        customList = []
        currentList = []
        
        placeCounter = 0
        #runPlace, runTime, playerName, runPoints
        while placeCounter < (len(self.portal_runs[chosenCat][chosenChamber].runs)):
            currentRun = self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].data

            runPlace = (self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["place"]) #Gets Player Place
            runTime = currentRun["times"]["primary_t"] #Gets Player Time
            playerName = ((self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].players)[0].name) #Gets Player Name
            #playerName = currentRun["players"][0]["uri"] #Not Working Other Way of getting Player Name
            #runTicks = (self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].ticks) #Gets Run Ticks?
            runPoints = (((50 - (runPlace - 1))**2) / 50) #Calculates Point Value

            try:
                runVidLink = currentRun["videos"]["links"][0]["uri"]#[0]["uri"]
            except:
                runVidLink = "N/A"

            runLink = currentRun["weblink"]
            runDate = currentRun["date"]

            currentList = [runPlace, playerName, runPoints, runTime, runLink, runVidLink, runDate] #creates single run entry list
            
            customList.append(currentList) #Adds that run to the full list
            placeCounter += 1

        return customList

    def createProfileListCategory(self, inputPlayerName, inputCategory):
        """Returns a 2D list of IL runs with points for a specific person for a specific category
        List Format: CATEGORY, CHAMBER, PLAYER, PLACE, POINTS, TIME"""

        userList = []

        for currentChamber in self.chamberList:
            currentList = []
            placeCounter = 0
            #runPlace, runTime, playerName, runPoints
            while placeCounter < (len(self.portal_runs[inputCategory][currentChamber].runs)):
                playerName = ((self.portal_runs[inputCategory][currentChamber].runs[placeCounter]["run"].players)[0].name) #Gets Player Name

                if(playerName == inputPlayerName):
                    currentRun = self.portal_runs[inputCategory][currentChamber].runs[placeCounter]["run"].data
                    runPlace = (self.portal_runs[inputCategory][currentChamber].runs[placeCounter]["place"])#Gets Player Place
                    runTime = currentRun["times"]["primary_t"] #Gets Player Time
                    runPoints = (((50 - (runPlace - 1))**2) / 50) #Calculates Point Value
                else:
                    placeCounter += 1
                    continue
                currentList = [inputCategory, currentChamber, runPlace, runPoints, runTime] #creates single run entry list

                userList.append(currentList) #Adds that run to the full profile list
                placeCounter += 1

        return userList

    def createProfileListAll(self, inputPlayerName):
        """Returns a 2D list of IL runs with points for a specific person for all categories
        List Format: CATEGORY, CHAMBER, PLAYER, PLACE, POINTS, TIME"""

        userList = []
        
        userList.extend(self.createProfileListCategory(inputPlayerName, "Out of Bounds"))
        userList.extend(self.createProfileListCategory(inputPlayerName, "Inbounds"))
        userList.extend(self.createProfileListCategory(inputPlayerName, "Glitchless"))

        return userList


    #Points Leaderboards
    def createAllCatPointsList(self):
        """Returns a points leaderboard of all players for all ILs"""
        
        fullList = []
        fullList.extend(self.createInboundsList())
        fullList.extend(self.createOobList())
        fullList.extend(self.createGlessList())

        userList = []
        currentRunIndex = 0
        while(currentRunIndex < (len(fullList))):
            searchUsername = 0
            if(currentRunIndex == 0): #Empty List adds first user from first run
                userList.append([fullList[currentRunIndex][2], fullList[currentRunIndex][4]])
            else:
                runFound = False
                while (searchUsername < (len(userList))):
                    if((fullList[currentRunIndex][2]) == userList[searchUsername][0]): #Duplicate User is found, add points
                        userList[searchUsername][1] += fullList[currentRunIndex][4]
                        runFound = True
                        break
                    searchUsername += 1

                if runFound != True: #User not currently in list, add to it
                    userList.append([fullList[currentRunIndex][2], fullList[currentRunIndex][4]])
            currentRunIndex += 1
        
        return userList

    def createSpecificCatPointsList(self, inputCategory):
        """Creates a points leaderboard of all players for all ILs of a specific category"""
        
        fullList = []
        if (inputCategory == "Inbounds"):
            fullList.extend(self.createInboundsList())
        elif(inputCategory == "Out of Bounds"):
            fullList.extend(self.createOobList())
        else:
            fullList.extend(self.createGlessList())

        userList = []
        currentRunIndex = 0
        while(currentRunIndex < (len(fullList))):
            searchUsername = 0
            if(currentRunIndex == 0): #Empty List adds first user from first run
                userList.append([fullList[currentRunIndex][2], fullList[currentRunIndex][4]])
            else:
                runFound = False
                while (searchUsername < (len(userList))):
                    if((fullList[currentRunIndex][2]) == userList[searchUsername][0]): #Duplicate User is found, add points
                        userList[searchUsername][1] += fullList[currentRunIndex][4]
                        runFound = True
                        break
                    searchUsername += 1

                if runFound != True: #User not currently in list, add to it
                    userList.append([fullList[currentRunIndex][2], fullList[currentRunIndex][4]])
            currentRunIndex += 1
        
        return userList


    #Point total retrieval
    def getPlayerTotalPointsAll(self, inputPlayerName):
        """Returns the total number of points a player has from all of their IL runs"""

        totalPoints = 0.0
        runCounter = 0
        userList = self.createProfileListAll(inputPlayerName)
        for runCounter in userList:
            totalPoints += runCounter[3]

        return totalPoints

    def getPlayerTotalPointsCategory(self, inputPlayerName, inputCategory):
        """Returns the total number of points a player has from a category of their IL runs"""

        totalPoints = 0.0
        runCounter = 0
        userList = self.createProfileListCategory(inputPlayerName, inputCategory)
        for runCounter in userList:
            totalPoints += runCounter[3]

        return totalPoints

    def getPlayerRanking(self, player):
        allCatsPointsList = self.createAllCatPointsList()
        df = pd.DataFrame(allCatsPointsList, columns = ['Player', 'Points'])
        df = df.sort_values('Points', ascending=False)
        df = df.round(decimals=2)

        df['Ranking'] = range(1, len(df) + 1) #Adds Ranking Column
        playerValues = df.loc[df['Player'] == player].values[0]
        playerValues = (f'{playerValues[2]},{playerValues[1]}')
        return playerValues

    def getPlayerRankingCategory(self, player, category):
        catPointsList = self.createSpecificCatPointsList(category)
        df = pd.DataFrame(catPointsList, columns = ['Player', 'Points'])
        df = df.sort_values('Points', ascending=False)
        df = df.round(decimals=2)

        df['Ranking'] = range(1, len(df) + 1) #Adds Ranking Column
    
        playerValues = df.loc[df['Player'] == player].values[0]
        playerValues = (f',{category},{playerValues[2]},{playerValues[1]}')
        return playerValues
        

    #Text Exports for Leaderboards
    def exportPointsLeaderboardText(self):
        """Returns text containing a points leaderboard of all players for all ILs of one or all categories
            Used in conjuction with either createAllCatPointsList or createSpecificCatPointsList
            Intended for use in the bot."""

        allCatsPointsList = self.createAllCatPointsList()

        fullText = "Place    |     Player    |     Total Points\n" 
        userCounter = 1
        for user in allCatsPointsList:
            userCounter + 1
            currentLine = (userCounter + " " + str(user[0]) + "  " + str(user[1]))
            fullText = fullText + currentLine + "\n"
        if(len(fullText) > 2000):
            fullText = fullText[0:1999]
            fullText = fullText[0:fullText.rfind("\n")]
        return fullText


    #Image Exports for Leaderboards
    def exportPointsLeaderboardImageDefault(self):
        """Saves an image containing a points leaderboard of all players for all ILs of one or all categories
            Used in conjuction with createAllCatPointsList
            Default Length of Leaderboard (10)
            Intended for use in the bot."""

        pio.kaleido.scope.default_height = 430 #Table Height

        allCatsPointsList = self.createAllCatPointsList() 
        df = pd.DataFrame(allCatsPointsList, columns = ['Player', 'Points'])
        df = df.sort_values('Points', ascending=False)
        df = df.round(decimals=2)

        df['Ranking'] = range(1, len(df) + 1) #Adds Ranking Column

        df = df.nsmallest(10, 'Ranking')

        #Using plotly to generate table and subsequent image
        fig = pgo.Figure(data=[pgo.Table(
            columnorder = [2,3,1],
            columnwidth = [60, 40, 25],
            header=dict(values=list(df.columns),
                        fill_color='#ffe196',
                        align='left'),
            cells=dict(values=[df.Player, df.Points, df.Ranking],
                    fill_color='#96e4ff',
                    align='left'))
        ])

        fig.write_image("list.png")

        listimg = Image.open("list.png")
        listimg = listimg.crop((80, 100, 620, 330))
        listimg.save("list.png")

    def exportPointsLeaderboardImage(self, boardLength):
        """Saves an image containing a points leaderboard of all players for all ILs or all categories
            Used in conjuction with createAllCatPointsList
            Uses Specified Length of Board
            Intended for use in the bot."""

        boardLength = int(boardLength)
        heightMult = 43 * boardLength 
        if (boardLength > 10):
            heightMult = heightMult - ((boardLength - 10) * 19)
        elif(boardLength < 6):
            heightMult = heightMult + 150
        elif(boardLength < 10):
            heightMult = heightMult + 100

        pio.kaleido.scope.default_height = heightMult

        allCatsPointsList = self.createAllCatPointsList()
        df = pd.DataFrame(allCatsPointsList, columns = ['Player', 'Points'])
        df = df.sort_values('Points', ascending=False)
        df = df.round(decimals=2)

        df['Ranking'] = range(1, len(df) + 1) #Adds Ranking Column

        df = df.nsmallest(boardLength, 'Ranking')

        #Using plotly to generate table and subsequent image
        fig = pgo.Figure(data=[pgo.Table(
            columnorder = [2,3,1],
            columnwidth = [60, 40, 25],
            header=dict(values=list(df.columns),
                        fill_color='#ffe196',
                        align='left'),
            cells=dict(values=[df.Player, df.Points, df.Ranking],
                    fill_color='#96e4ff',
                    align='left'))
        ])

        fig.write_image("list.png")

        listimg = Image.open("list.png")
        listimg = listimg.crop((80, 100, 620, (heightMult-100)))
        listimg.save("list.png")

    def exportPointsLeaderboardImageMax(self):
        """Saves an image containing a points leaderboard of all players for all ILs of one or all categories
            Used in conjuction with createAllCatPointsList
            Max Length of Board
            Intended for use in the bot."""

        pio.kaleido.scope.default_height = 3350

        allCatsPointsList = self.createAllCatPointsList()
        df = pd.DataFrame(allCatsPointsList, columns = ['Player', 'Points'])
        df = df.sort_values('Points', ascending=False)
        df = df.round(decimals=2)

        df['Ranking'] = range(1, len(df) + 1) #Adds Ranking Column

        #Using plotly to generate table and subsequent image
        fig = pgo.Figure(data=[pgo.Table(
            columnorder = [2,3,1],
            columnwidth = [60, 40, 25],
            header=dict(values=list(df.columns),
                        fill_color='#ffe196',
                        align='left'),
            cells=dict(values=[df.Player, df.Points, df.Ranking],
                    fill_color='#96e4ff',
                    align='left'))
        ])

        fig.write_image("list.png")

        listimg = Image.open("list.png")
        listimg = listimg.crop((80, 100, 620, 3000))
        listimg.save("list.png")

    def exportCatPointsLeaderboardImageDefault(self, category):
        """Saves an image containing a points leaderboard of all players for all ILs of one category
            Used in conjuction with createSpecificCatPointsList
            Default Length of Leaderboard (10)
            Intended for use in the bot."""

        pio.kaleido.scope.default_height = 430 #Table Height

        catPointsList = self.createSpecificCatPointsList(category) 
        df = pd.DataFrame(catPointsList, columns = ['Player', 'Points'])
        df = df.sort_values('Points', ascending=False)
        df = df.round(decimals=2)

        df['Ranking'] = range(1, len(df) + 1) #Adds Ranking Column

        df = df.nsmallest(10, 'Ranking')

        #Using plotly to generate table and subsequent image
        fig = pgo.Figure(data=[pgo.Table(
            columnorder = [2,3,1],
            columnwidth = [60, 40, 25],
            header=dict(values=list(df.columns),
                        fill_color='#ffe196',
                        align='left'),
            cells=dict(values=[df.Player, df.Points, df.Ranking],
                    fill_color='#96e4ff',
                    align='left'))
        ])

        fig.write_image("list.png")

        listimg = Image.open("list.png")
        listimg = listimg.crop((80, 100, 620, 330))
        listimg.save("list.png")

    def exportCatPointsLeaderboardImage(self, category, boardLength):
        """Saves an image containing a points leaderboard of all players for all ILs of one category
            Used in conjuction with createSpecificCatPointsList
            Uses Specified Length of Board
            Intended for use in the bot."""

        boardLength = int(boardLength)
        heightMult = 43 * boardLength 
        if (boardLength > 10):
            heightMult = heightMult - ((boardLength - 10) * 19)
        elif(boardLength < 6):
            heightMult = heightMult + 150
        elif(boardLength < 10):
            heightMult = heightMult + 100

        pio.kaleido.scope.default_height = heightMult

        catPointsList = self.createSpecificCatPointsList(category) 
        df = pd.DataFrame(catPointsList, columns = ['Player', 'Points'])
        df = df.sort_values('Points', ascending=False)
        df = df.round(decimals=2)

        df['Ranking'] = range(1, len(df) + 1) #Adds Ranking Column

        df = df.nsmallest(boardLength, 'Ranking')

        #Using plotly to generate table and subsequent image
        fig = pgo.Figure(data=[pgo.Table(
            columnorder = [2,3,1],
            columnwidth = [60, 40, 25],
            header=dict(values=list(df.columns),
                        fill_color='#ffe196',
                        align='left'),
            cells=dict(values=[df.Player, df.Points, df.Ranking],
                    fill_color='#96e4ff',
                    align='left'))
        ])

        fig.write_image("list.png")

        listimg = Image.open("list.png")
        listimg = listimg.crop((80, 100, 620, (heightMult-100)))
        listimg.save("list.png")

    def exportChamberPointsLeaderboardImage(self, category, level):
        """Returns an image containing a points leaderboard of all players for one IL of one category
            Used in conjuction with createSpecificChamberListBetter
            Variable Length of Board
            Intended for use in the bot."""

        catPointsList = self.createSpecificChamberListBot(category, level) 
        df = pd.DataFrame(catPointsList, columns = ['Place', 'Player', 'Points', 'Time'])
        df = df.sort_values('Points', ascending=False)
        df = df.round(decimals=2)

        boardLength = len(df)
        heightMult = 43 * boardLength 
        if (boardLength > 10):
            heightMult = heightMult - ((boardLength - 10) * 19)
        elif(boardLength < 6):
            heightMult = heightMult + 150
        elif(boardLength < 10):
            heightMult = heightMult + 100

        pio.kaleido.scope.default_height = heightMult

        #Using plotly to generate table and subsequent image
        fig = pgo.Figure(data=[pgo.Table(
            #title=f"{category} {level}",
            #font=dict(family="verdana", font_size=15),
            columnorder = [1,2,3,4],
            columnwidth = [25, 60, 40, 40],
            header=dict(values=list(df.columns),
                        fill_color='#ffe196',
                        align='left'),
            cells=dict(values=[df.Place, df.Player, df.Points, df.Time],
                    fill_color='#96e4ff',
                    align='left'),)
        ])

        fig.write_image("list.png")

        listimg = Image.open("list.png")
        listimg = listimg.crop((80, 100, 620, (heightMult-100)))
        listimg.save("list.png")
    
    def exportPlayerProfileDefault(self, player):
        """Saves an image containing a player's top 5 ILs of all categories
            Used in conjuction with createProfileListAll
            Default Length of Leaderboard (5)
            Intended for use in the bot."""

        pio.kaleido.scope.default_height = 380 #Table Height

        allCatsPointsList = self.createProfileListAll(player) 
        df = pd.DataFrame(allCatsPointsList, columns = ['Category', 'Chamber', 'Place', 'Points', 'Time'])
        df = df.sort_values('Points', ascending=False)
        totalPoints = int(df['Points'].sum())
        df.Points = df.Points.round(decimals=2)

        df = df.nsmallest(5, 'Place')

        #Using plotly to generate table and subsequent image
        fig = pgo.Figure(data=[pgo.Table(
            columnorder = [1,2,3,4,5],
            columnwidth = [25, 25, 25, 25, 25],
            header=dict(values=list(df.columns),
                        fill_color='#ffe196',
                        align='left'),
            cells=dict(values=[df.Category, df.Chamber, df.Place, df.Points, df.Time],
                    fill_color='#96e4ff',
                    align='left'))
        ])

        fig.write_image("list.png")

        listimg = Image.open("list.png")
        listimg = listimg.crop((80, 100, 620, 230))
        listimg.save("list.png")
        return totalPoints

    def exportPlayerProfileCategory(self, player, category):
        """Saves an image containing a player's top 10 ILs of a single category
            Used in conjuction with createProfileListAll
            Default Length of Leaderboard (10)
            Intended for use in the bot."""
        pio.kaleido.scope.default_height = 430 #Table Height

        allCatsPointsList = self.createProfileListCategory(player, category) 
        df = pd.DataFrame(allCatsPointsList, columns = ['Category', 'Chamber', 'Place', 'Points', 'Time'])
        df = df.sort_values('Points', ascending=False)
        totalPoints = int(df['Points'].sum())
        df.Points = df.Points.round(decimals=2)
        df.Time = df.Time.round(decimals=3)
        df = df.nsmallest(10, 'Place')
        
        #Using plotly to generate table and subsequent image
        fig = pgo.Figure(data=[pgo.Table(
            columnorder = [1,2,3,4,5],
            columnwidth = [25, 25, 25, 25, 25],
            header=dict(values=list(df.columns),
                        fill_color='#ffe196',
                        align='left'),
            cells=dict(values=[df.Category, df.Chamber, df.Place, df.Points, df.Time],
                    fill_color='#96e4ff',
                    align='left'))
        ])

        fig.write_image("list.png")

        listimg = Image.open("list.png")
        listimg = listimg.crop((80, 100, 620, 330))
        listimg.save("list.png")
        return totalPoints

    def exportPlayerProfileCategoryAll(self, player, category):
        '''Saves an image containing a player's top 10 ILs of a single category
            Used in conjuction with createProfileListAll
            Default Length of Leaderboard (5)
            Intended for use in the bot.'''

        allCatsPointsList = self.createProfileListCategory(player, category) 
        df = pd.DataFrame(allCatsPointsList, columns = ['Category', 'Chamber', 'Place', 'Points', 'Time'])
        df = df.sort_values('Points', ascending=False)
        totalPoints = int(df['Points'].sum())
        df.Points = df.Points.round(decimals=2)

        boardLength = int(df.size / 5)
        heightMult = 43 * boardLength
        if (boardLength > 10):
            heightMult = heightMult - ((boardLength - 10) * 19)
        elif(boardLength < 6):
            heightMult = heightMult + 150
        elif(boardLength < 10):
            heightMult = heightMult + 100

        pio.kaleido.scope.default_height = heightMult

        advQuery = df.query('Chamber.str.startswith("Adv")')
        advQuery = advQuery.sort_values('Chamber')
        escQuery = df.query('Chamber.str.startswith("e")')
        escQuery = escQuery.sort_values('Chamber')
        numQuery = df.query('Chamber.str.startswith("1") or Chamber.str.startswith("0")')
        numQuery = numQuery.sort_values('Chamber')

        df = pd.concat([numQuery, escQuery, advQuery])

        #Using plotly to generate table and subsequent image
        fig = pgo.Figure(data=[pgo.Table(
            columnorder = [1,2,3,4,5],
            columnwidth = [25, 25, 25, 25, 25],
            header=dict(values=list(df.columns),
                        fill_color='#ffe196',
                        align='left'),
            cells=dict(values=[df.Category, df.Chamber, df.Place, df.Points, df.Time],
                    fill_color='#96e4ff',
                    align='left'))
        ])

        fig.write_image("list.png")

        listimg = Image.open("list.png")
        listimg = listimg.crop((80, 100, 620, (heightMult-100)))
        listimg.save("list.png")
        return totalPoints


    #Don't work rn
    def exportPointsLeaderboardImageArrow(self, currentHighestPlayer):
        """Saves an image containing a points leaderboard of all players for all ILs of one or all categories
            Used in conjuction with createAllCatPointsList
            Default Length of Leaderboard (10)
            Intended for use in the bot."""

        pio.kaleido.scope.default_height = 430 #Table Height

        allCatsPointsList = self.createAllCatPointsList() 
        df = pd.DataFrame(allCatsPointsList, columns = ['Player', 'Points'])
        df = df.sort_values('Points', ascending=False)
        df = df.round(decimals=2)

        df['Ranking'] = range(1, len(df) + 1) #Adds Ranking Column

        df = df[df.Ranking <= currentHighestPlayer and df.Ranking >= currentHighestPlayer - 10]

        #Using plotly to generate table and subsequent image
        fig = pgo.Figure(data=[pgo.Table(
            columnorder = [2,3,1],
            columnwidth = [60, 40, 25],
            header=dict(values=list(df.columns),
                        fill_color='#ffe196',
                        align='left'),
            cells=dict(values=[df.Player, df.Points, df.Ranking],
                    fill_color='#96e4ff',
                    align='left'))
        ])

        fig.write_image("list.png")

        listimg = Image.open("list.png")
        listimg = listimg.crop((80, 100, 620, 330))
        listimg.save("list.png")

    def exportCatPointsLeaderboardImageArrow(self, category, currentHighestPlayer):
        """Saves an image containing a points leaderboard of all players for all ILs of one category
            Used in conjuction with createSpecificCatPointsList
            Default Length of Leaderboard (10)
            Intended for use in the bot."""

        pio.kaleido.scope.default_height = 430 #Table Height

        catPointsList = self.createSpecificCatPointsList(category) 
        df = pd.DataFrame(catPointsList, columns = ['Player', 'Points'])
        df = df.sort_values('Points', ascending=False)
        df = df.round(decimals=2)

        df['Ranking'] = range(1, len(df) + 1) #Adds Ranking Column

        df = df[df.Ranking <= currentHighestPlayer and df.Ranking >= currentHighestPlayer - 10]

        #Using plotly to generate table and subsequent image
        fig = pgo.Figure(data=[pgo.Table(
            columnorder = [2,3,1],
            columnwidth = [60, 40, 25],
            header=dict(values=list(df.columns),
                        fill_color='#ffe196',
                        align='left'),
            cells=dict(values=[df.Player, df.Points, df.Ranking],
                    fill_color='#96e4ff',
                    align='left'))
        ])

        fig.write_image("list.png")

        listimg = Image.open("list.png")
        listimg = listimg.crop((80, 100, 620, 330))
        listimg.save("list.png")

    #Commands
    def leaderboardCommand(self, userMessage):
        '''Command used for the bot to make overall points leaderboards
        Includes specification of category, length, and of both category and length'''

        boardLength = 10 #Default Leaderboard Length
        
        #!Leaderboard [NUMBER], !Leaderboard Max, and !Leaderboard [CATEGORY]
        if (len(userMessage) == 2): 

            #!Leaderboard [NUMBER] creates specified length leaderboard
            if (userMessage[1].isnumeric()): #numeric leaderboard requests(i.e. 15, 100)
                boardLength = int(userMessage[1])

                if boardLength < 300 and boardLength > 1:
                    try:
                        self.exportPointsLeaderboardImage(boardLength)
                        return f"Top {boardLength} Overall Players"

                    except:
                        print('SRC is prolly pooping its pants')
                        return "fail"
                else:
                    return "lengthfail"

            else: #Non-numeric leaderboard requests(i.e. max, inbounds, oob)
                #!Leaderboard max creates whole leaderboard
                if (userMessage[1].lower() == "max"):
                        try:
                            self.exportPointsLeaderboardImageMax()
                            return "All Players Overall"
                        except:
                            print('SRC is prolly pooping its pants')
                            return "fail"

                #!Leaderboard [CATEGORY] creates specific category leaderboard
                elif (userMessage[1].lower() == "inbounds" or userMessage[1].lower() == "inbob" or \
                        userMessage[1].lower() == "oob" or userMessage[1].lower() == "gless" or userMessage[1].lower() == "glitchless"):
                    try:
                        category = userMessage[1]
                        category = self.inputToCategory(category)
                        if(category == ''):
                            return("catfail")

                        self.exportCatPointsLeaderboardImageDefault(category)

                        return f"Top {category} Players"

                    except:
                        print('SRC is prolly pooping its pants')
                        return "fail"

                else:
                    return "modfail"
                        
        
        elif (len(userMessage) == 3): #Leaderboard [CATEGORY] [NUMBER] creates a specific category leaderboard of specific length
            try:
                category = userMessage[1]
                category = self.inputToCategory(category)

                userMessage[2].isnumeric()
                if(category == ''):
                    return("catfail")

                elif(not(int(userMessage[2]) > 0 and int(userMessage[2]) < 300 and userMessage[2].isnumeric())):
                    return("lengthfail")

                boardLength = int(userMessage[2])
                self.exportCatPointsLeaderboardImage(category, boardLength)
                return f"Top {boardLength} {category} Players"

            except:
                print('SRC is prolly pooping its pants')
                return "fail"


        else: #!Leaderboard
            try:
                #!Leaderboard creates default length (10) leaderboard
                self.exportPointsLeaderboardImageDefault()
                return f"Top Overall Players"
            except:
                print('SRC is prolly pooping its pants')
                return "fail"

    def levelboardCommand(self, userMessage):
        '''Command used for the bot to make level leaderboards
        Includes required specification of category and chamber'''

        category = userMessage[1]
        level = userMessage[2]
        if(len(userMessage) == 4):
            level = (userMessage[2] + userMessage[3]).replace(' ', '')
        
        category = self.inputToCategory(category)
        level = self.inputToChamber(level)

        if(category == '' or level == ''):
            if(category == ''):
                return("catfail")
            elif(level == ''):
                return ("chamberfail")
            else:
                return("fail")

        try:
            self.exportChamberPointsLeaderboardImage(category, level)
            return(f"**{category} {level} Leaderboard:**")

        except:
            return("fail")

    def userprofileCommand(self, userMessage):
        '''Command used for the bot to make a user profile
        !Profile [PLAYER]
        Includes user's top 5 runs, overall place w/ total points, and place w/ points for each cat 
        !Profile [PLAYER] [CATEGORY]
        or top 10 runs of a specific cat and points 
        !Profile [PLAYER] [CATEGORY] ALL
        or all runs from a specific cat.'''

        if (len(userMessage) == 1):
            #Not Implemented
            pass

        elif (len(userMessage) == 2):
            #!Profile [PLAYER]
            try:
                playerRanking = self.getPlayerRanking(userMessage[1])
                missingCats = 0
                catRanks = ""
                for category in self.catList:
                    try:
                        currentCatRank = self.getPlayerRankingCategory(userMessage[1], category)
                        catRanks = catRanks + currentCatRank

                    except:
                        missingCats += 1
                        print(f"Player Doesn't have {category} ILs")

                if (missingCats >= 3):
                    return("namefail")

                self.exportPlayerProfileDefault(userMessage[1])
                totalPoints = playerRanking
                return (str(totalPoints) + str(catRanks))

            except:
                return 'srcfail'

        elif (len(userMessage) == 3):
            #!Profile [PLAYER] [CATEGORY]
            try:
                player = userMessage[1]
                category = userMessage[2]
                category = self.inputToCategory(category)

                if(category == ''):
                    return("catfail")

                playerRanking = self.getPlayerRankingCategory(player, category)
                self.exportPlayerProfileCategory(player, category)

                return playerRanking

            except:
                return 'srcfail'

        elif (len(userMessage) == 4):
            #!Profile [PLAYER] [CATEGORY] ALL
            try:
                player = userMessage[1]
                category = userMessage[2]
                category = self.inputToCategory(category)

                if(category == ''):
                    return("catfail")

                playerRanking = self.getPlayerRankingCategory(player, category)
                self.exportPlayerProfileCategoryAll(player, category)

                return playerRanking

            except:
                return 'srcfail'

        else:
            #invalid length
            return 'fail'

    def runCommand(self, userMessage):
        '''Command used for the bot to return information on a run
        !Run [PLAYER] [CATEGORY] [CHAMBER]'''

        try:
            player = userMessage[1]
            category = userMessage[2]
            level = userMessage[3]
            if(len(userMessage) == 5):
                level = (userMessage[3] + userMessage[4]).replace(' ', '')

            category = self.inputToCategory(category)
            level = self.inputToChamber(level)

            if(category == '' or level == '' or player == ''):
                return("fail")

            catPointsList = self.createSpecificChamberListMore(category, level) 
            
            df = pd.DataFrame(catPointsList, columns = ['Place', 'Player', 'Points', 'Time', 'Link', 'Video', 'Date'])
            df = df.sort_values('Points', ascending=False)
            df = df.round(decimals=2)

            runValues = (df.loc[df['Player'] == player].values)[0]
            runPlace = runValues[0]
            runPoints = runValues[2]
            runTime = runValues[3]
            runLink  = runValues[4]
            runVid = runValues[5]
            runDate  = runValues[6]
            runValues = [player, category, level, runPlace, runPoints, runTime, runLink, runVid, runDate]
            return(runValues)

        except:
            return "fail"


    #Input Filtering

    def inputToCategory(self, userCategory):
        '''Takes input and converts it to correctly formatted category name'''
        userCategory = userCategory.lower()

        if(userCategory == "inbob" or userCategory == "inbounds"): #Inbounds
            return ("Inbounds")

        elif(userCategory == "oob"): #Out of Bounds
            return ("Out of Bounds")

        elif(userCategory == "gless" or userCategory == "glitchless"): #Glitchless
            return ("Glitchless")

        else:
            return("")

    def inputToChamber(self, userChamber):
        '''Takes input and converts it to correctly formatted chamber name'''
        userChamber = userChamber.replace('/','')
        userChamber = userChamber.replace('-','')

        if (userChamber == '10'):
            return(self.chamberList[6]) #10
        else:
            userChamber = userChamber.replace('0','')

        if('adv' in userChamber):
            userChamber = userChamber.replace('anced', '')

            if(userChamber == 'adv13'):
                return(self.chamberList[18]) #adv13
            elif(userChamber == 'adv14'):
                return(self.chamberList[19]) #adv14
            elif(userChamber == 'adv15'):
                return(self.chamberList[20]) #adv15
            elif(userChamber == 'adv16'):
                return(self.chamberList[21]) #adv16
            elif(userChamber == 'adv17'):
                return(self.chamberList[22]) #adv17
            elif(userChamber == 'adv18'):
                return(self.chamberList[23]) #adv18
            else:
                return('')

        elif ('e' in userChamber):
            if (userChamber == 'e'):
                return(self.chamberList[15]) #e00
            elif (userChamber == 'e1'):
                return(self.chamberList[16]) #e01
            elif (userChamber == 'e2'):
                return(self.chamberList[17]) #e02
            else:
                return('')

        else: 
            if (userChamber == '' or userChamber == '1' or userChamber.lower() == "owo"):
                return(self.chamberList[0]) #00-01
            elif (userChamber == '23' or userChamber == '2' or userChamber == '3'):
                return(self.chamberList[1]) #02-03
            elif (userChamber == '45' or userChamber == '4' or userChamber == '5'):
                return(self.chamberList[2]) #04-05
            elif(userChamber == '67' or userChamber == '6' or userChamber == '7'):
                return(self.chamberList[3]) #06-07
            elif(userChamber == '8'):
               return(self.chamberList[4]) #08
            elif (userChamber == '9'):
                return(self.chamberList[5]) #09
            elif (userChamber == '1112' or userChamber == '11' or userChamber == '12'):
                return(self.chamberList[7]) #11-12
            elif (userChamber == '13'):
                return(self.chamberList[8]) #13
            elif (userChamber == '14'):
                return(self.chamberList[9]) #14
            elif (userChamber == '15'):
                return(self.chamberList[10]) #15
            elif (userChamber == '16'):
                return(self.chamberList[11]) #16
            elif (userChamber == '17'):
                return(self.chamberList[12]) #17
            elif (userChamber == '18'):
                return(self.chamberList[13]) #18
            elif (userChamber == '19'):
                return(self.chamberList[14]) #19
            elif(userChamber == '10'):
                pass
            else:
                return('')

    #Don't work rn
    def leaderboardArrowCommand(self, userMessage, currentHighestPlayer):
        '''Command used for the bot to make overall points leaderboards after a reaction'''

        boardLength = 10 #Default Leaderboard Length
        
        #!Leaderboard [CATEGORY] after a reaction
        if (len(userMessage) == 2): 
            try:
                if(userMessage[1].lower() == "inbob" or userMessage[1].lower() == "inbounds"): #Inbounds
                    self.exportCatPointsLeaderboardImageArrow("Inbounds", currentHighestPlayer)

                elif(userMessage[1].lower() == "oob"): #Out of Bounds
                    self.exportCatPointsLeaderboardImageArrow("Out of Bounds", currentHighestPlayer)

                elif(userMessage[1].lower() == "gless" or userMessage[1].lower() == "glitchless"): #Glitchless
                    self.exportCatPointsLeaderboardImageArrow("Glitchless", currentHighestPlayer)

                return "success"

            except:
                print('SRC is prolly pooping its pants')
                return "fail"                 

        else: #!Leaderboard after a reaction
            try:
                #!Leaderboard creates default length (10) leaderboard
                self.exportPointsLeaderboardImageArrow(currentHighestPlayer)
                return "success"

            except:
                print('SRC is prolly pooping its pants')
                return "fail"

