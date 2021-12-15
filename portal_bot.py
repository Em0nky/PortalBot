from discord import user
from discord.abc import Messageable
import asyncio
from PortalPointsSlim import PortalPoints
import discord

#PortalBot V0.0.2

#Points Pre-Setup
PP = PortalPoints()


client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    #Default Hello Command
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')


    #Testing Command
    if message.content.startswith('!portal'):
        await message.channel.send('Yes Portal')


    #General Points Leaderboard Commands
    if message.content.startswith('!Leaderboard') or message.content.startswith('!leaderboard') or \
            message.content.startswith('!lb') or message.content.startswith('!LB'):

        userMessage = message.content.split(" ")
        try:
            boardCreated = PP.leaderboardCommand(userMessage)
        except:
            await message.channel.send('Invalid Leaderboard Command.')
        
        if (boardCreated.startswith("Top") or boardCreated.startswith("All")): #Success
            #List Image
            file = discord.File("list.png")
            embed = discord.Embed(description=f"**{boardCreated}**")
            embed.set_image(url="attachment://list.png")
            await message.channel.send(embed=embed, file=file)

        elif (boardCreated == "lengthfail"): #Fail
            await message.channel.send('Invalid Leaderboard Length.')

        elif (boardCreated == "modfail"): #Fail
            await message.channel.send('Invalid Leaderboard Modifier. !help lb')

        elif (boardCreated == "catfail"): #Fail
            await message.channel.send('Invalid Category.')

        else: #Fail
            await message.channel.send('Something Went Wrong (Likely the SRC API)')
            

    #Chamber Points Leaderboard Commands
    if message.content.startswith('!Levelboard') or message.content.startswith('!lvlb') or\
        message.content.startswith('!levelboard'):

        userMessage = message.content.split(" ")
        try:
            boardCreated = PP.levelboardCommand(userMessage)

        except:
            await message.channel.send('Invalid Leaderboard Command.')
        
        if ("Glitchless" in boardCreated or "Out of Bounds" in boardCreated or "Inbounds" in boardCreated): #Success
            file = discord.File("list.png")
            embed = discord.Embed(description=f"**{boardCreated}**")
            embed.set_image(url="attachment://list.png")
            await message.channel.send(embed=embed, file=file)

        elif (boardCreated == "chamberfail"): #Fail
            await message.channel.send('Invalid Chamber. !help lb')

        elif (boardCreated == "catfail"): #Fail
            await message.channel.send('Invalid Category. !help lb')

        else: #Fail
            await message.channel.send('Invalid Command.')


    #Profile Commands
    if message.content.startswith('!profile') or message.content.startswith('!pf') or\
        message.content.startswith('!Profile') or message.content.startswith('!Pf'):

        userMessage = message.content.split(" ")
        
        try:
            profileCreated = PP.userprofileCommand(userMessage)
        except:
            await message.channel.send('Invalid Profile Command.')
        
        if (len(profileCreated) == 4):
            playerID = str(profileCreated[2])
            playerName = str(profileCreated[3])
            profileCreatedS = profileCreated[0] + profileCreated[1]
            profileCreatedS = profileCreatedS.split(",")

            file = discord.File("list.png")
            embed = embedProfile(userMessage, profileCreatedS, playerID, playerName)
            embed.set_image(url="attachment://list.png")
            await message.channel.send(embed=embed, file=file)
        
        elif(len(profileCreated) == 3):
            playerID = str(profileCreated[1])
            playerName = str(profileCreated[2])
            profileCreatedS = profileCreated[0]
            profileCreatedS = profileCreatedS.split(",")

            file = discord.File("list.png")
            embed = embedProfile(userMessage, profileCreatedS, playerID, playerName)
            embed.set_image(url="attachment://list.png")
            await message.channel.send(embed=embed, file=file)

        elif (profileCreated == 'namefail'):
            await message.channel.send(f'No Player named \"{userMessage[1]}\" has IL Runs or Doesn\'t Exist')

        elif (profileCreated == 'catfail'):
            await message.channel.send('Invalid Category.')

        elif (profileCreated == 'missfail'):
            await message.channel.send(f'No Player named \"{userMessage[1]}\" has IL Runs in That Category or Doesn\'t Exist')

        elif (profileCreated == 'srcfail'):
            await message.channel.send('Error Retrieving Submission.')


        else:
            await message.channel.send("Invalid Profile Command.")


    #Run Command
    if message.content.startswith('!Run') or message.content.startswith('!run'):
        userMessage = message.content.split(" ")

        if(len(userMessage) == 4 or len(userMessage) == 5):
            runInfo = PP.runCommand(userMessage)
            if(len(runInfo) == 10):
                embed = embedRun(runInfo)
                await message.channel.send(embed=embed)

            elif(runInfo == "fail"):
                await message.channel.send('Error Retrieving Submission.')

            else:
                await message.channel.send('Run May Not Exist.')

        else:
            await message.channel.send("Invalid Run Command")


    #Help Command
    if (message.content).lower() == ('!help'):
        embed = discord.Embed(description=f"**List of Commands for PortalBot:**")
        embed.add_field(name="**Leaderboards: **", value="!Leaderboard(or !lb) [*optional*] [*optional*]", inline=False)
        embed.add_field(name="**Levelboards: **", value="!Levelboard(or !lvlb) [*category*] [*level*]", inline=False)
        embed.add_field(name="**User Profile: **", value="!Profile(or !pf) [*player name*] [*optional*] [*optional*]", inline=False)
        embed.add_field(name="**Run: **", value="!Run [*player name*] [*category*] [*level*]", inline=False)
        embed.add_field(name="**For Help with Specific Commands Use:**", value="\"!help [command]\" ex. \"!help *leaderboard*\"", inline=False)
        await message.channel.send(embed=embed)
    

    #Specific Help Commands
    if message.content.startswith('!help '):
        userMessage = (message.content.lower()).split(" ")

        if (userMessage[1] == "leaderboard") or (userMessage[1] == "lb"): #!Leaderboard
            embed = discord.Embed(description=f"**!Leaderboard (or !lb) Can Be Used to Display a Particular Point Leaderboard**")
            embed.add_field(name="**!Leaderboard (Default Command):**", value="This returns an overall points leaderboard of the top 10 runners.", inline=False)
            embed.add_field(name="**!Leaderboard Max:**", value="This returns an overall points leaderboard of all runners. (This is really tall)", inline=False)
            embed.add_field(name="**!Leaderboard [NUMBER]:**", value="ex. \"!lb *15*\": This returns an overall points leaderboard of the top [NUMBER] runners.", inline=False)
            embed.add_field(name="**!Leaderboard [CATEGORY]:**", value="ex. \"!lb *inbounds*\": This returns a points leaderboard for the specified category of the top 10 runners.", inline=False)
            embed.add_field(name="**!Leaderboard [CATEGORY] [NUMBER]:**", value="ex. \"!lb *inbounds 25*\": This returns a points leaderboard for the specified category of the top [NUMBER] runners.", inline=False)
            embed.add_field(name="** **", value="**Instructions on Leaderboards of Runs for a Specific Chamber can be Found with \"!help levelboard\"**", inline=False)
            await message.channel.send(embed=embed)

        elif (userMessage[1] == "levelboard") or (userMessage[1] == "lvlb"): #!Levelboard
            embed = discord.Embed(description=f"**!Levelboard (or !lvlb) Can Be Used to Display a Particular Level's Point Leaderboard**", inline=False)
            embed.add_field(name="**!Levelboard [CATEGORY] [LEVEL]:**", value="ex. \"!lvlb *inbounds 00/01*: This returns the level's points leaderboard.", inline=False)
            await message.channel.send(embed=embed)

        elif (userMessage[1] == "profile") or (userMessage[1] == "pf"): #!Profile
            embed = discord.Embed(description=f"**!Profile (or !pf) Can Be Used to Get Different Information or Lists for a Specific Runner**")
            embed.add_field(name="**!Profile (Default Command):**", value="This returns a linked user's top 5 runs and total points. **NOT IMPLEMENTED**", inline=False)
            embed.add_field(name="**!Profile [PLAYER]**", value="ex. \"!Profile *Shizzal*\": This returns the user's top 5 runs, overall place w/ total points, and place w/ points for each cat.", inline=False)
            embed.add_field(name="**!Profile [PLAYER] [CATEGORY]**", value="ex. \"!Profile *Shizzal* *Inbounds*\": This returns the user's top 10 runs from the category, overall place in the cat and points.", inline=False)
            embed.add_field(name="**!Profile [PLAYER] [CATEGORY] All**", value="ex. \"!Profile *Shizzal* *Inbounds* All\": This returns all the user's runs from the category, overall place in the cat and points.", inline=False)
            await message.channel.send(embed=embed)

        elif (userMessage[1] == "run"): #!Run
            embed = discord.Embed(description=f"**!Run Can Be Used to Get a Specific IL Run for a Specific Runner**")
            embed.add_field(name="**!Run [PLAYER] [CATEGORY] [CHAMBER]**", value="ex. !run *RealCreative oob 08*: This returns information on a user's run on a specific IL.", inline=False)
            await message.channel.send(embed=embed)

        else: #Incorrect Entry
            await message.channel.send(f"No Such Command \"!{userMessage[1]}\" Exists")


def embedProfile(userMessage, profileCreated, playerID, playerName):
    pName = playerName

    if(len(userMessage) == 2):
        oPoints = profileCreated[1]
        cat1 = profileCreated[2]
        points1 = profileCreated[4]
        oPlace = profileCreated[0]
        place1 = profileCreated[3]

        embed = discord.Embed(description="")
        if(playerID == ""):
            embed.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.freebiesupply.com%2Flogos%2Flarge%2F2x%2Fportal-9-logo-png-transparent.png&f=1&nofb=1")
            embed.set_author(name=f"{pName}'s Profile:")
        else:
            embed.set_thumbnail(url=f"https://www.speedrun.com/userasset/{playerID}/image?v=3d18eec")
            embed.set_author(name=f"{pName}'s Profile:", url=f"https://www.speedrun.com/user/{playerName}")
            
        embed.add_field(name=f"**Overall Points:**", value= f"{oPoints}", inline=False)
        embed.add_field(name=f"**{cat1} Points:**", value= f"{points1}", inline=True)

        if(len(profileCreated) == 5):
            embed.add_field(name=f"\n**Overall Place:**", value= f"{oPlace}", inline=False)
            embed.add_field(name=f"**{cat1} Place:**", value= f"{place1}", inline=True)

        if(len(profileCreated) == 8):
            cat2 = profileCreated[5]
            points2 = profileCreated[7]
            place2 = profileCreated[6]

            embed.add_field(name=f"**{cat2} Points:**", value= f"{points2}", inline=True)
            embed.add_field(name=f"\n**Overall Place:**", value= f"{oPlace}", inline=False)
            embed.add_field(name=f"**{cat1} Place:**", value= f"{place1}", inline=True)
            embed.add_field(name=f"**{cat2} Place:**", value= f"{place2}", inline=True)
            

        elif(len(profileCreated) == 11):
            cat2 = profileCreated[5]
            points2 = profileCreated[7]
            place2 = profileCreated[6]
            cat3 = profileCreated[8]
            points3 = profileCreated[10]
            place3 = profileCreated[9]

            embed.add_field(name=f"**{cat2} Points:**", value= f"{points2}", inline=True)
            embed.add_field(name=f"**{cat3} Points:**", value= f"{points3}", inline=True)
            embed.add_field(name=f"\n**Overall Place:**", value= f"{oPlace}", inline=False)
            embed.add_field(name=f"**{cat1} Place:**", value= f"{place1}", inline=True)
            embed.add_field(name=f"**{cat2} Place:**", value= f"{place2}", inline=True)
            embed.add_field(name=f"**{cat3} Place:**", value= f"{place3}", inline=True)

    elif(len(userMessage) == 3) or (len(userMessage) == 4):
        cat1 = profileCreated[1]
        points = profileCreated[3]
        place = profileCreated[2]

        embed = discord.Embed(description="")
        if(playerID == ""):
            embed.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.freebiesupply.com%2Flogos%2Flarge%2F2x%2Fportal-9-logo-png-transparent.png&f=1&nofb=1")
            embed.set_author(name=f"{pName}'s {cat1} Profile:")
        else:
            embed.set_thumbnail(url=f"https://www.speedrun.com/userasset/{playerID}/image?v=3d18eec")
            embed.set_author(name=f"{pName}'s {cat1} Profile:", url=f"https://www.speedrun.com/user/{playerName}")

        embed.add_field(name=f"**{cat1} Points:**", value= f"{points}", inline=True)
        embed.add_field(name=f"**{cat1} Place:**", value= f"{place}", inline=True)

    return embed


def embedRun(runInfo):
    pName = runInfo[0]
    cat = runInfo[1]
    chamber = runInfo[2]
    place = runInfo[3]
    points = runInfo[4]
    time = runInfo[5]
    date = runInfo[8]
    runLink = runInfo[6]
    vidLink = runInfo[7]
    playerID = runInfo[9]
    runTicks = (float(time)/.015)

    if(vidLink == "N/A"):
        embed = discord.Embed(description=f"[Run]({runLink}) | N/A")
    else:
        embed = discord.Embed(description=f"[Run]({runLink}) | [Video]({vidLink})")

    if(playerID == ""):
        embed.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.freebiesupply.com%2Flogos%2Flarge%2F2x%2Fportal-9-logo-png-transparent.png&f=1&nofb=1")
        embed.set_author(name=f"{pName}'s {cat} {chamber} Run")
    else:
        embed.set_thumbnail(url=f"https://www.speedrun.com/userasset/{playerID}/image?v=3d18eec")
        embed.set_author(name=f"{pName}'s {cat} {chamber} Run", url=f"https://www.speedrun.com/user/{pName}")

    if(place == 1):
        embed.add_field(name="**Place**", value=":trophy: 1", inline=True)
    else:
        embed.add_field(name="**Place**", value=f"{place}", inline=True)

    embed.add_field(name="**Points**", value=f"{points}", inline=True)
    embed.add_field(name="**Date**", value=f"{date}", inline=False)
    embed.add_field(name="**Time**", value=f"{time}", inline=True)
    embed.add_field(name="**Ticks**", value=f"{runTicks:.0f}", inline=True)
    

    return embed


tokenFile = open("botToken.txt", "r")

client.run(tokenFile.read())
