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
                runPlace = (self.portal_runs["Inbounds"][currentChamber].runs[placeCounter]["place"]) #Gets Player Place
                runTime = (self.portal_runs["Inbounds"][currentChamber].runs[placeCounter]["run"].times["primary_t"]) #Gets Player Time
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
                runPlace = (self.portal_runs["Out of Bounds"][currentChamber].runs[placeCounter]["place"]) #Gets Player Place
                runTime = (self.portal_runs["Out of Bounds"][currentChamber].runs[placeCounter]["run"].times["primary_t"]) #Gets Player Time
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
                runPlace = (self.portal_runs["Glitchless"][currentChamber].runs[placeCounter]["place"]) #Gets Player Place
                runTime = (self.portal_runs["Glitchless"][currentChamber].runs[placeCounter]["run"].times["primary_t"]) #Gets Player Time
                playerName = ((self.portal_runs["Glitchless"][currentChamber].runs[placeCounter]["run"].players)[0].name) #Gets Player Name
                runPoints = (((50 - (runPlace - 1))**2) / 50) #Calculates Point Value

                currentList = ["Glitchless", currentChamber, playerName, runPlace, runPoints, runTime] #creates single run entry list

                glessList.append(currentList) #Adds that run to the full list
                placeCounter += 1

        return glessList

    def createSpecificChamberList(self):
        """Returns a 2D list of runs for a specific chamber of a specific category
        List Format: CATEGORY, CHAMBER, PLAYER, PLACE, POINTS, TIME"""

        customList = []
        currentList = []

        chosenCat = input("Enter a Category: ")
        chosenChamber = input("Enter a Chamber[00-01, 08, e02, etc...]: ")
        
        placeCounter = 0

        #runPlace, runTime, playerName, runPoints
        while placeCounter < (len(self.portal_runs[chosenCat][chosenChamber].runs)):
            runPlace = (self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["place"]) #Gets Player Place
            runTime = (self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].times["primary_t"]) #Gets Player Time
            playerName = ((self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].players)[0].name) #Gets Player Name
            runPoints = (((50 - (runPlace - 1))**2) / 50) #Calculates Point Value

            currentList = [chosenCat, chosenChamber, playerName, runPlace, runPoints, runTime] #creates single run entry list

            customList.append(currentList) #Adds that run to the full list
            placeCounter += 1

        return customList

    def createSpecificChamberListBetter(self, chosenCat, chosenChamber):
        """Returns a 2D list of runs for a specific chamber of a specific category using arguments
        List Format: CATEGORY, CHAMBER, PLAYER, PLACE, POINTS, TIME"""

        customList = []
        currentList = []
        
        placeCounter = 0

        #runPlace, runTime, playerName, runPoints
        while placeCounter < (len(self.portal_runs[chosenCat][chosenChamber].runs)):
            runPlace = (self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["place"]) #Gets Player Place
            runTime = (self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].times["primary_t"]) #Gets Player Time
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
            runPlace = (self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["place"]) #Gets Player Place
            runTime = (self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].times["primary_t"]) #Gets Player Time
            playerName = ((self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].players)[0].name) #Gets Player Name
            #runTicks = (self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].ticks) #Gets Run Ticks?
            runPoints = (((50 - (runPlace - 1))**2) / 50) #Calculates Point Value

            currentList = [runPlace, playerName, runPoints, runTime] #creates single run entry list
            
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
                    runPlace = (self.portal_runs[inputCategory][currentChamber].runs[placeCounter]["place"]) #Gets Player Place
                    runTime = (self.portal_runs[inputCategory][currentChamber].runs[placeCounter]["run"].times["primary_t"]) #Gets Player Time
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
        print("poopy")
        print(f'Overall,{playerValues[2]},{playerValues[1]}')
        playerValues = (f'{playerValues[2]},{playerValues[1]}')
        return playerValues

    def getPlayerRankingCategory(self, player, category):
        catPointsList = self.createSpecificCatPointsList(category)
        df = pd.DataFrame(catPointsList, columns = ['Player', 'Points'])
        df = df.sort_values('Points', ascending=False)
        df = df.round(decimals=2)

        df['Ranking'] = range(1, len(df) + 1) #Adds Ranking Column
    
        playerValues = df.loc[df['Player'] == player].values[0]
        print(f',{category},{playerValues[2]},{playerValues[1]}')
        playerValues = (f',{category},{playerValues[2]},{playerValues[1]}')
        return playerValues
        


    #CSV file exports for leaderboards
    def exportPointsLeaderboardCSV(inputLeaderboard, leaderboardFileName):
        """Exports a CSV file containing a points leaderboard of all players for all ILs of one or all categories
            Used in conjuction with either createAllCatPointsList or createSpecificCatPointsList"""

        fullLeaderboard = ""

        f = open(leaderboardFileName, "w", encoding="utf-8") #open

        for user in inputLeaderboard:
            currentLine = (str(user[0]) + "," + str(user[1]))
            fullLeaderboard = fullLeaderboard + currentLine + "\n"

        f.write(fullLeaderboard)

        f.close #close

    def exportPlayerProfileCSV(inputLeaderboard, leaderboardFileName):
        """Exports a CSV file containing a profile of a single player for all ILs
            Used in conjunction with either createProfileListAll or creatProfileListCategory"""

        fullLeaderboard = ""
        currentLine = ""

        f = open(leaderboardFileName, "w", encoding="utf-8") #open

        for user in inputLeaderboard:
            currentLine = user[0] + "," + user[1] + "," + str(user[2]) + "," + str(user[3]) + "," + str(user[4])
            fullLeaderboard = fullLeaderboard + currentLine + "\n"

        f.write(fullLeaderboard)

        f.close #close

    def exportTheBigSheet(self, leaderboardFileName):
        """Exports a formatted sheet of points leaderboard, level leaderboards, and player profiles"""
        #Bolded, points, Multiple Bolded, level leaderboards, bolded, player profile

        #Categories
        catList = ["Inbounds", "Out of Bounds", "Glitchless"]
        listOfPlayers = []
        fullText = ""
        allCatsPointsList = self.createAllCatPointsList()

        f = open(leaderboardFileName, "w", encoding="utf-8") #open


        #All Cats Points Board
        fullText = "Points Board\n" + "Player,Total Points\n" 
        for user in allCatsPointsList:
            currentLine = (str(user[0]) + "," + str(user[1]))
            fullText = fullText + currentLine + "\n"
            listOfPlayers.append(user[0])

        fullText = fullText + "\n\n" #Spacing New Line


        #Individual Cat Points Boards
        currentCategory = ""
        for currentCategory in catList:
            fullText += (currentCategory + " Points List\n")
            fullText += " Player,Total Points\n"
            currentCatPointsList = self.createSpecificCatPointsList(currentCategory)

            for user in currentCatPointsList:
                currentLine = (str(user[0]) + "," + str(user[1]))
                fullText = fullText + currentLine + "\n"

            fullText = fullText + "\n\n" #Spacing New Line


        #Individual Chamber Boards
        currentBoard = []
        currentCategory = ""
        for currentCategory in catList:
            currentChamber = ""
            for currentChamber in self.chamberList:
                currentIndex = ""
                currentBoard = self.createSpecificChamberListBetter(currentCategory, currentChamber)
                for currentIndex in currentBoard:
                    currentLine = (currentIndex[0] + "," + str(currentIndex[1]) + "," + currentIndex[2] + "," + str(currentIndex[3]) + "," + str(currentIndex[4]) + "," + str(currentIndex[5]) + "\n")
                    fullText = fullText + currentLine
                fullText = fullText + "\n"

        
        #Player Profiles
        for player in listOfPlayers: #Loop Through All Players
            fullText += (player + "'s Profile\n") #Player Name

            for currentCategory in catList: #Loop Through all Categories for Player
                currentPlayerCurrentCat = self.createProfileListCategory(player, currentCategory)
                if len(currentPlayerCurrentCat) == 0:
                    continue
                fullText += (currentCategory + ",Chamber,Place,Points,Time\n") #Category List Name
                

                for user in currentPlayerCurrentCat: #Loop Through All ILs in Category
                    currentLine = user[0] + "," + user[1] + "," + str(user[2]) + "," + str(user[3]) + "," + str(user[4])
                    fullText = fullText + currentLine + "\n"
            fullText += "\n" #Spacing Between Players New Line

        f.write(fullText)

        f.close #close

    def exportSubSheets(self):
        """Exports formatted sheets of points leaderboard, level leaderboards, and player profiles"""
        #Bolded, points, Multiple Bolded, level leaderboards, bolded, player profile

        #Categories
        catList = ["Inbounds", "Out of Bounds", "Glitchless"]
        listOfPlayers = []

        #Text for assignment to csv files
        fullText = ""
        overText = ""
        inbobText = ""
        oobText = ""
        glessText = ""
        inbobLText = "Category,Level,Player,Place,Points,Time\n"
        oobLText = "Category,Level,Player,Place,Points,Time\n"
        glessLText = "Category,Level,Player,Place,Points,Time\n"
        userText = ""

        allCatsPointsList = self.createAllCatPointsList()

        fOverall = open("OverallBoard.csv", "w", encoding="utf-8") #open
        fInbounds = open("InboundsBoard.csv", "w", encoding="utf-8") #open
        fInboundsLevels = open("InboundsLevelsBoard.csv", "w", encoding="utf-8") #open
        fOOB = open("OOBBoard.csv", "w", encoding="utf-8") #open
        fOOBLevels = open("OOBLevelsBoard.csv", "w", encoding="utf-8") #open
        fGless = open("GlessBoard.csv", "w", encoding="utf-8") #open
        fGlessLevels = open("GlessLevelsBoard.csv", "w", encoding="utf-8") #open
        fUsers = open("Users.csv", "w", encoding="utf-8") #open
        fUsersFormat = open("UsersFormat.csv", "w", encoding="utf-8") #open

        #All Cats Points Board -> Sheet 1
        fullText = "Player,Total Points\n" 
        for user in allCatsPointsList:
            currentLine = (str(user[0]) + "," + str(user[1]))
            fullText = fullText + currentLine + "\n"
            listOfPlayers.append(user[0])
        overText = fullText
        fullText = ""

        #Individual Cat Points Boards -> Start of Sheets 2,3,4
        currentCategory = ""
        for currentCategory in catList:
            fullText += " Player,Total Points\n"
            currentCatPointsList = self.createSpecificCatPointsList(currentCategory)

            for user in currentCatPointsList:
                currentLine = (str(user[0]) + "," + str(user[1]))
                fullText = fullText + currentLine + "\n"

            if currentCategory == "Inbounds":
                inbobText = fullText + "\n"
            elif currentCategory == "Out of Bounds":
                oobText = fullText + "\n"
            else:
                glessText = fullText + "\n"
            fullText = "" 


        #Individual Chamber Boards -> Sheets 2,3,4
        currentBoard = []
        currentCategory = ""
        for currentCategory in catList:
            currentChamber = ""
            for currentChamber in self.chamberList:
                currentIndex = ""
                currentBoard = self.createSpecificChamberListBetter(currentCategory, currentChamber)
                for currentIndex in currentBoard:
                    currentLine = (currentIndex[0] + "," + str(currentIndex[1]) + "," + currentIndex[2] + "," + str(currentIndex[3]) + "," + str(currentIndex[4]) + "," + str(currentIndex[5]) + "\n")
                    fullText = fullText + currentLine
                fullText = fullText + "\n"

            if currentCategory == "Inbounds":
                inbobLText = inbobLText + fullText
            elif currentCategory == "Out of Bounds":
                oobLText = oobLText + fullText
            else:
                glessLText = glessLText + fullText
            fullText = ""

        
        #Player Profiles -> Sheet 5
        for player in listOfPlayers: #Loop Through All Players
            #fullText += (player + "'s Profile\n") #Player Name

            for currentCategory in catList: #Loop Through all Categories for Player
                currentPlayerCurrentCat = self.createProfileListCategory(player, currentCategory)
                if len(currentPlayerCurrentCat) == 0:
                    continue
                fullText += ("Player" + "," + currentCategory + ",Chamber,Place,Points,Time\n") #Category List Name
                

                for user in currentPlayerCurrentCat: #Loop Through All ILs in Category
                    currentLine = player + "," + user[0] + "," + user[1] + "," + str(user[2]) + "," + str(user[3]) + "," + str(user[4])
                    fullText = fullText + currentLine + "\n"
            fullText += "\n" #Spacing Between Players New Line

        userText = fullText

        fOverall.write(overText)
        fInbounds.write(inbobText)
        fOOB.write(oobText)
        fGless.write(glessText)
        fUsers.write(userText)
        fInboundsLevels.write(inbobLText)
        fOOBLevels.write(oobLText)
        fGlessLevels.write(glessLText)

        fOverall.close #close
        fInbounds.close #close
        fOOB.close #close
        fGless.close #close
        fInboundsLevels.close #close
        fOOBLevels.close #close
        fGlessLevels.close #close
        fUsers.close #close


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
        print("other one")
        pio.kaleido.scope.default_height = 430 #Table Height

        allCatsPointsList = self.createProfileListCategory(player, category) 
        df = pd.DataFrame(allCatsPointsList, columns = ['Category', 'Chamber', 'Place', 'Points', 'Time'])
        df = df.sort_values('Points', ascending=False)
        totalPoints = int(df['Points'].sum())
        df.Points = df.Points.round(decimals=2)
        df.Time = df.Time.round(decimals=3)
        df = df.nsmallest(10, 'Place')
        print("imagine")
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
        """Saves an image containing a player's top 10 ILs of a single category
            Used in conjuction with createProfileListAll
            Default Length of Leaderboard (5)
            Intended for use in the bot."""
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
                        catString = ""

                        if(userMessage[1].lower() == "inbob" or userMessage[1].lower() == "inbounds"): #Inbounds
                            self.exportCatPointsLeaderboardImageDefault("Inbounds")
                            catString = "Inbounds"

                        elif(userMessage[1].lower() == "oob"): #Out of Bounds
                            self.exportCatPointsLeaderboardImageDefault("Out of Bounds")
                            catString = "Out of Bounds"

                        elif(userMessage[1].lower() == "gless" or userMessage[1].lower() == "glitchless"): #Glitchless
                            self.exportCatPointsLeaderboardImageDefault("Glitchless")
                            catString = "Glitchless"

                        return f"Top {catString} Players"

                    except:
                        print('SRC is prolly pooping its pants')
                        return "fail"

                else:
                    return "modfail"
                        
        
        elif (len(userMessage) == 3): #Leaderboard [CATEGORY] [NUMBER] creates a specific category leaderboard of specific length
            if ((userMessage[1].lower() == "inbounds" or userMessage[1].lower() == "inbob" or userMessage[1].lower() == "inbound" or \
                    userMessage[1].lower() == "oob" or userMessage[1].lower() == "gless" or userMessage[1].lower() == "glitchless")\
                    and int(userMessage[2]) > 0 and int(userMessage[2]) < 300 and userMessage[2].isnumeric()):
                try:
                    catString = ""

                    boardLength = int(userMessage[2])
                    if(userMessage[1].lower() == "inbob" or userMessage[1].lower() == "inbounds"): #Inbounds
                        self.exportCatPointsLeaderboardImage("Inbounds", boardLength)
                        catString = "Inbounds"

                    elif(userMessage[1].lower() == "oob"): #Out of Bounds
                        self.exportCatPointsLeaderboardImage("Out of Bounds", boardLength)
                        catString = "Out of Bounds"

                    elif(userMessage[1].lower() == "gless" or userMessage[1].lower() == "glitchless"): #Glitchless
                        self.exportCatPointsLeaderboardImage("Glitchless", boardLength)
                        catString = "Glitchless"

                    return f"Top {boardLength} {catString} Players"

                except:
                    print('SRC is prolly pooping its pants')
                    return "fail"

            else:
                return "modfail"

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

        validChamber = True

        if (len(userMessage) == 3 and userMessage[2].isnumeric()):
            levelShort = userMessage[2].replace('/','')
            levelShort = levelShort.replace('-','')
            levelShort = levelShort.replace(' ','')
            if (levelShort == '10'):
                levelShort = self.chamberList[6] #10
            else:
                levelShort = levelShort.replace('0','')
            if ('e' in levelShort):
                if (levelShort == 'e'):
                    levelShort = self.chamberList[15] #e00
                elif (levelShort == 'e1'):
                    levelShort = self.chamberList[16] #e01
                elif (levelShort == 'e2'):
                    levelShort = self.chamberList[17] #e02
            else: 
                if (levelShort == '' or levelShort == '1' or levelShort.lower() == "owo"):
                    levelShort = self.chamberList[0] #00-01
                elif (levelShort == '23' or levelShort == '2' or levelShort == '3'):
                    levelShort = self.chamberList[1] #02-03
                elif (levelShort == '45' or levelShort == '4' or levelShort == '5'):
                    levelShort = self.chamberList[2] #04-05
                elif(levelShort == '67' or levelShort == '6' or levelShort == '7'):
                    levelShort = self.chamberList[3] #06-07
                elif(levelShort == '8'):
                    levelShort = self.chamberList[4] #08
                elif (levelShort == '9'):
                    levelShort = self.chamberList[5] #09
                elif (levelShort == '1112' or levelShort == '11' or levelShort == '12'):
                    levelShort = self.chamberList[7] #11-12
                elif (levelShort == '13'):
                    levelShort = self.chamberList[8] #13
                elif (levelShort == '14'):
                    levelShort = self.chamberList[9] #14
                elif (levelShort == '15'):
                    levelShort = self.chamberList[10] #15
                elif (levelShort == '16'):
                    levelShort = self.chamberList[11] #16
                elif (levelShort == '17'):
                    levelShort = self.chamberList[12] #17
                elif (levelShort == '18'):
                    levelShort = self.chamberList[13] #18
                elif (levelShort == '19'):
                    levelShort = self.chamberList[14] #19
                elif(levelShort == '10'):
                    pass
                else:
                    validChamber = False
                    return "chamberfail"
                
                if(validChamber == True):
                    try:
                        if(userMessage[1].lower() == "inbob" or userMessage[1].lower() == "inbounds"): #Inbounds
                            listTitle = "Inbounds " + str(levelShort)
                            self.exportChamberPointsLeaderboardImage("Inbounds", levelShort)

                        elif(userMessage[1].lower() == "oob"): #Out of Bounds
                            listTitle = "Out of Bounds " + str(levelShort)
                            self.exportChamberPointsLeaderboardImage("Out of Bounds", levelShort)

                        elif(userMessage[1].lower() == "gless" or userMessage[1].lower() == "glitchless"): #Glitchless
                            listTitle = "Glitchless " + str(levelShort)
                            self.exportChamberPointsLeaderboardImage("Glitchless", levelShort)

                        else:
                            validChamber = False
                            return "catfail"

                        if(validChamber == True):
                            return listTitle

                    except:
                        return "fail"

        else:
            levelShort = userMessage[2]

            if(len(userMessage) == 4):
                levelShort = str(userMessage[2]) + str(userMessage[3])
            if('adv' in levelShort or 'advanced' in levelShort):
                levelShort = levelShort.replace('anced', '')
                if(levelShort == 'adv13'):
                    levelShort = self.chamberList[18] #adv13
                elif(levelShort == 'adv14'):
                    levelShort = self.chamberList[19] #adv14
                elif(levelShort == 'adv15'):
                    levelShort = self.chamberList[20] #adv15
                elif(levelShort == 'adv16'):
                    levelShort = self.chamberList[21] #adv16
                elif(levelShort == 'adv17'):
                    levelShort = self.chamberList[22] #adv17
                elif(levelShort == 'adv18'):
                    levelShort = self.chamberList[23] #adv18
                else:
                    validChamber = False
                    return("chamberfail")

            if(validChamber == True):
                    try:
                        if(userMessage[1].lower() == "inbob" or userMessage[1].lower() == "inbounds"): #Inbounds
                            listTitle = "Inbounds " + str(levelShort)
                            self.exportChamberPointsLeaderboardImage("Inbounds", levelShort)

                        elif(userMessage[1].lower() == "oob"): #Out of Bounds
                            listTitle = "Out of Bounds " + str(levelShort)
                            self.exportChamberPointsLeaderboardImage("Out of Bounds", levelShort)

                        elif(userMessage[1].lower() == "gless" or userMessage[1].lower() == "glitchless"): #Glitchless
                            listTitle = "Glitchless " + str(levelShort)
                            self.exportChamberPointsLeaderboardImage("Glitchless", levelShort)

                        else:
                            validChamber = False
                            return("catfail")

                        if(validChamber == True):
                            return listTitle

                    except:
                        print('SRC is prolly pooping its pants')
            else:
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
                
                try:
                    if(userMessage[2].lower() == "glitchless" or userMessage[2].lower() == "gless"):
                        playerRanking = self.getPlayerRankingCategory(userMessage[1], "Glitchless")
                        self.exportPlayerProfileCategory(userMessage[1], "Glitchless")

                    elif(userMessage[2].lower() == "inbounds" or userMessage[2].lower() == "inbob"):
                        playerRanking = self.getPlayerRankingCategory(userMessage[1], "Inbounds")
                        self.exportPlayerProfileCategory(userMessage[1], "Inbounds")

                    elif(userMessage[2].lower() == "oob"):
                        playerRanking = self.getPlayerRankingCategory(userMessage[1], "Out of Bounds")
                        self.exportPlayerProfileCategory(userMessage[1], "Out of Bounds")
                    
                    else:
                        return 'catfail'

                except:
                    return 'missfail'

                return playerRanking

            except:
                return 'srcfail'


        elif (len(userMessage) == 4):
            #!Profile [PLAYER] [CATEGORY] ALL
            try:
                
                try:
                    if(userMessage[2].lower() == "glitchless" or userMessage[2].lower() == "gless"):
                        playerRanking = self.getPlayerRankingCategory(userMessage[1], "Glitchless")
                        self.exportPlayerProfileCategoryAll(userMessage[1], "Glitchless")

                    elif(userMessage[2].lower() == "inbounds" or userMessage[2].lower() == "inbob"):
                        playerRanking = self.getPlayerRankingCategory(userMessage[1], "Inbounds")
                        self.exportPlayerProfileCategoryAll(userMessage[1], "Inbounds")

                    elif(userMessage[2].lower() == "oob"):
                        playerRanking = self.getPlayerRankingCategory(userMessage[1], "Out of Bounds")
                        self.exportPlayerProfileCategoryAll(userMessage[1], "Out of Bounds")
                    
                    else:
                        return 'catfail'

                except:
                    return 'missfail'

                return playerRanking

            except:
                return 'srcfail'


        else:
            #invalid length
            return 'fail'


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

