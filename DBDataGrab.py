import srcomapi, srcomapi.datatypes as dt
import csv

api = srcomapi.SpeedrunCom(); api.debug = 1

class PortalPoints:
    """
    Class for accessing SRC api in order to assign points to IL placements
    """

    def __init__(self):
        """
        Constructor, Grabs API stuff and creates below lists:
        catList, chamberList, chamberListNoAdv, and chamberListOnlyAdv
        
        """
        
        #Grabbing Information from SRC
        apiSuccessGrab = False
        while(apiSuccessGrab == False):
            try: 
                apiSuccessGrab = True
                #api stuff kinda scuffed
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
                runPoints = self.pointsCalculation(runPlace)

                currentList = ["Inbounds", currentChamber, playerName, runPlace, runPoints, runTime] #Creates single run entry list

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
                runPoints = self.pointsCalculation(runPlace)

                currentList = ["Out of Bounds", currentChamber, playerName, runPlace, runPoints, runTime] #Creates single run entry list

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
                runPoints = self.pointsCalculation(runPlace)

                currentList = ["Glitchless", currentChamber, playerName, runPlace, runPoints, runTime] #Creates single run entry list

                glessList.append(currentList) #Adds that run to the full list
                placeCounter += 1

        return glessList


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
            runTicks = (runTime/.015)
            playerName = ((self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].players)[0].name) #Gets Player Name
            try:
                playerID = ((self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].players)[0].id) #Gets Player ID
            except:
                playerID = ""

            #playerName = currentRun["players"][0]["uri"] #Not Working Other Way of getting Player Name
            #runTicks = (self.portal_runs[chosenCat][chosenChamber].runs[placeCounter]["run"].ticks) #Supposed to get ticks
            runPoints = self.pointsCalculation(runPlace)

            try:
                runVidLink = currentRun["videos"]["links"][0]["uri"]#[0]["uri"]
            except:
                runVidLink = "N/A"
            runLink = currentRun["weblink"]
            runDate = currentRun["date"]

            currentList = [chosenCat, chosenChamber, runPlace, playerName, playerID, runTime, runTicks, runPoints, runDate, runLink, runVidLink] #creates single run entry list
            
            customList.append(currentList) #Adds that run to the full list
            placeCounter += 1

        return customList
        
    #Points Leaderboards
    def createAllCatPointsList(self):
        """Returns a points leaderboard of all players for all ILs"""
        
        fullList = []
        for category in self.catList:
            for level in self.chamberList:
                fullList.extend(self.createSpecificChamberListMore(category, level))
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(fullList)
        print("AAAAAAAAAAAAAAAAAAAAAAAAA")

        userList = []
        userList.append(["RunnerID", "RunnerID"])
        currentRunIndex = 0
        while(currentRunIndex < (len(fullList))):
            searchUsername = 0
            if(currentRunIndex == 0): #Empty List adds first user from first run
                userList.append([fullList[currentRunIndex][3], fullList[currentRunIndex][4]])
            else:
                runFound = False
                while (searchUsername < (len(userList))):
                    if((fullList[currentRunIndex][3]) == userList[searchUsername][0]): #Duplicate User is found, add points
                        runFound = True
                        break
                    searchUsername += 1

                if runFound != True: #User not currently in list, add to it
                        userList.append([fullList[currentRunIndex][3], fullList[currentRunIndex][4]])
            currentRunIndex += 1
        
        return userList

    def createAllRuns(self):
        fullList = []
        for category in self.catList:
            for level in self.chamberList:
                fullList.extend(self.createSpecificChamberListMore(category, level))

        print(fullList)
        return fullList

    def pointsCalculation(self, runPlace):
        if runPlace > 50:
            return 0

        linearPoints = 51 - runPlace #Calculates Point Value
        expPoints = (((50 - (runPlace - 1))**2)/50)
        expPoints = round(expPoints,2)
        
        if expPoints < 1:
            expPoints = 1

        finalPoints = ((expPoints + linearPoints)/2)
        finalPoints = round(finalPoints, 2)

        return finalPoints

pp = PortalPoints()

uList = pp.createAllCatPointsList()

with open('userList.csv', 'w', encoding='utf-8') as f:
    write = csv.writer(f)
    write.writerows(uList)

rList = [["Category", "Chamber", "Place", "RunnerName", "SRCID", "Time", "Ticks", "Points", "Date", "Link", "VideoLink"]] 
rList.extend(pp.createAllRuns())


with open('runList.csv', 'w', encoding='utf-8') as f:
    write = csv.writer(f)
    write.writerows(rList)
