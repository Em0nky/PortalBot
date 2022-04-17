import time
from DBHelper import DBHelper
import discord

# PortalBot V0.3.3

# Points Pre-Setup
dbHelper = DBHelper()
client = discord.Client()


@client.event
async def on_ready():
    print('Successfully logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    # If message is from bot, don't do anything
    if message.author == client.user:
        return

    # General Points Leaderboard Commands
    if message.content.lower().startswith('!leaderboard') or message.content.lower().startswith('!lb'):

        # TODO create variable for args instead of changing the message variable to an array
        # args = message.content.split(" ")

        message = message.content.split(" ")

        try:
            board_created = dbHelper.leaderboardCommand(message)
        except:
            await message.channel.send('Invalid Leaderboard Command.')

        if board_created.lower().startswith("top") or board_created.lower().startswith("all"):

            # List Image
            file = discord.File("list.png")
            embed = discord.Embed(description=f"**{board_created}**")
            embed.set_image(url="attachment://list.png")
            await message.channel.send(embed=embed, file=file)

        # Error Messages
        elif board_created == "lengthfail":
            await message.channel.send('Invalid leaderboard length.')

        elif board_created == "modfail":
            await message.channel.send('Invalid leaderboard modifier. !help lb')

        elif board_created == "catfail":
            await message.channel.send('Invalid category.')

        else:
            await message.channel.send('Something went wrong. Please try again later.')

    # Chamber Points Leaderboard Commands
    if message.content.lower().startswith('!levelboard') or message.content.lower().startswith('!lvlb'):

        message = message.content.split(" ")

        try:
            board_created = dbHelper.levelboardCommand(message)
        except:
            await message.channel.send('Invalid Leaderboard Command.')

        if "Glitchless" or "Out of Bounds" or "Inbounds" in board_created:

            file = discord.File("list.png")
            embed = discord.Embed(description=f"**{board_created}**")
            embed.set_image(url="attachment://list.png")
            await message.channel.send(embed=embed, file=file)

        # Error messages

        elif board_created == "chamberfail":
            await message.channel.send('Invalid Chamber. !help lb')

        elif board_created == "catfail":
            await message.channel.send('Invalid Category. !help lb')

        else:
            await message.channel.send('Invalid Command.')

    # Profile Commands
    if message.content.lower().startswith('!profile') or message.content.lower().startswith('!pf'):

        message = message.content.split(" ")

        try:
            profile_created = dbHelper.userprofileCommand(message)
            print(profile_created)
        except:
            await message.channel.send('Invalid Profile Command.')

        if len(profile_created) == 4:
            playerID = str(profile_created[2])
            playerName = str(profile_created[3])
            profileCreatedS = profile_created[0] + profile_created[1]
            profileCreatedS = profileCreatedS.split(",")

            file = discord.File("list.png")
            embed = embedProfile(message, profileCreatedS, playerID, playerName)
            embed.set_image(url="attachment://list.png")
            await message.channel.send(embed=embed, file=file)

        elif len(profile_created) == 3:

            playerID = str(profile_created[1])
            playerName = str(profile_created[2])
            profileCreatedS = profile_created[0]
            profileCreatedS = profileCreatedS.split(",")

            file = discord.File("list.png")
            embed = embedProfile(message, profileCreatedS, playerID, playerName)
            embed.set_image(url="attachment://list.png")
            await message.channel.send(embed=embed, file=file)

        elif profile_created == 'namefail':
            await message.channel.send(f'No Player named \"{message[1]}\" has IL Runs or doesn\'t Exist')

        elif profile_created == 'catfail':
            await message.channel.send('Invalid Category.')

        elif profile_created == 'missfail':
            await message.channel.send(f'No Player named \"{message[1]}\" has IL Runs in That Category or doesn\'t Exist')

        elif profile_created == 'srcfail':
            await message.channel.send('Error Retrieving Submission.')

        else:
            await message.channel.send("Invalid Profile Command.")

    # Run Command
    if message.content.lower().startswith('!run'):

        message = message.content.split(" ")

        if len(message) == 4 or len(message) == 5:

            runInfo = dbHelper.runCommand(message)

            if len(runInfo) == 10:
                embed = embedRun(runInfo)
                await message.channel.send(embed=embed)

            elif runInfo == "fail":
                await message.channel.send('Error Retrieving Submission.')

            else:
                await message.channel.send('Run May Not Exist.')

        else:
            await message.channel.send("Invalid Run Command")

    # Recent Command
    if message.content.lower().startswith('!recent'):

        message = message.content.split(" ")

        try:

            recentCreated = dbHelper.recentCommand(message)
            file = discord.File("list.png")

            if len(recentCreated) == 1:
                embed = discord.Embed(description=f"**{recentCreated[0]}'s Recent 10 Overall Runs:**")
                embed.set_image(url="attachment://list.png")
                await message.channel.send(embed=embed, file=file)

            elif len(recentCreated) == 2:
                embed = discord.Embed(description=f"**{recentCreated[0]}'s Recent 10 {recentCreated[1]} Runs:**")
                embed.set_image(url="attachment://list.png")
                await message.channel.send(embed=embed, file=file)

            else:
                if recentCreated == 'srcfail':
                    await message.channel.send('Error Retrieving Submission.')

                elif recentCreated == 'catfail':
                    await message.channel.send('Invalid Category.')

                else:
                    await message.channel.send('Invalid Recent Command.')

        except:
            await message.channel.send('Invalid Recent Command.')

    # Help Command
    if message.content.lower() == '!help':

        embed = discord.Embed(description=f"**List of Commands for PortalBot:**")
        embed.add_field(name="**Leaderboards: **", value="!Leaderboard(or !lb) [*optional*] [*optional*]", inline=False)
        embed.add_field(name="**Levelboards: **", value="!Levelboard(or !lvlb) [*category*] [*level*]", inline=False)
        embed.add_field(name="**User Profile: **", value="!Profile(or !pf) [*player name*] [*optional*] [*optional*]",
                        inline=False)
        embed.add_field(name="**Run: **", value="!Run [*player name*] [*category*] [*level*]", inline=False)
        embed.add_field(name="**Recent: **", value="!Recent [*player name*] [*optional*]", inline=False)
        embed.add_field(name="**For Help with Specific Commands Use:**",
                        value="\"!help [command]\" ex. \"!help *leaderboard*\"", inline=False)
        await message.channel.send(embed=embed)

    # Specific Help Commands
    if message.content.startswith('!help '):

        message = message.content.lower().split(" ")

        if (message[1] == "leaderboard") or (message[1] == "lb"):
            embed = discord.Embed(
                description=f"**!Leaderboard (or !lb) Can Be Used to Display a Particular Point Leaderboard**")
            embed.add_field(name="**!Leaderboard (Default Command):**",
                            value="This returns an overall points leaderboard of the top 10 runners.", inline=False)
            embed.add_field(name="**!Leaderboard Max:**",
                            value="This returns an overall points leaderboard of all runners. (This is really tall)",
                            inline=False)
            embed.add_field(name="**!Leaderboard [NUMBER]:**",
                            value="ex. \"!lb *15*\": This returns an overall points leaderboard of the top [NUMBER] runners.",
                            inline=False)
            embed.add_field(name="**!Leaderboard [CATEGORY]:**",
                            value="ex. \"!lb *inbounds*\": This returns a points leaderboard for the specified category of the top 10 runners.",
                            inline=False)
            embed.add_field(name="**!Leaderboard [CATEGORY] [NUMBER]:**",
                            value="ex. \"!lb *inbounds 25*\": This returns a points leaderboard for the specified category of the top [NUMBER] runners.",
                            inline=False)
            embed.add_field(name="** **",
                            value="**Instructions on Leaderboards of Runs for a Specific Chamber can be Found with \"!help levelboard\"**",
                            inline=False)
            await message.channel.send(embed=embed)

        elif (message[1] == "levelboard") or (message[1] == "lvlb"):  # !Levelboard
            embed = discord.Embed(
                description=f"**!Levelboard (or !lvlb) Can Be Used to Display a Particular Level's Point Leaderboard**",
                inline=False)
            embed.add_field(name="**!Levelboard [CATEGORY] [LEVEL]:**",
                            value="ex. \"!lvlb *inbounds 00/01*: This returns the level's points leaderboard.",
                            inline=False)
            await message.channel.send(embed=embed)

        elif (message[1] == "profile") or (message[1] == "pf"):  # !Profile
            embed = discord.Embed(
                description=f"**!Profile (or !pf) Can Be Used to Get Different Information or Lists for a Specific Runner**")
            embed.add_field(name="**!Profile (Default Command):**",
                            value="This returns a linked user's top 5 runs and total points. **NOT IMPLEMENTED**",
                            inline=False)
            embed.add_field(name="**!Profile [PLAYER]**",
                            value="ex. \"!Profile *Shizzal*\": This returns the user's top 5 runs, overall place w/ total points, and place w/ points for each cat.",
                            inline=False)
            embed.add_field(name="**!Profile [PLAYER] [CATEGORY]**",
                            value="ex. \"!Profile *Shizzal* *Inbounds*\": This returns the user's top 10 runs from the category, overall place in the cat and points.",
                            inline=False)
            embed.add_field(name="**!Profile [PLAYER] [CATEGORY] All**",
                            value="ex. \"!Profile *Shizzal* *Inbounds* All\": This returns all the user's runs from the category, overall place in the cat and points.",
                            inline=False)
            await message.channel.send(embed=embed)

        elif message[1] == "run":  # !Run
            embed = discord.Embed(description=f"**!Run Can Be Used to Get a Specific IL Run for a Specific Runner**")
            embed.add_field(name="**!Run [PLAYER] [CATEGORY] [CHAMBER]**",
                            value="ex. !run *RealCreative oob 08*: This returns information on a user's run on a specific IL.",
                            inline=False)
            await message.channel.send(embed=embed)

        elif message[1] == "recent":  # !Recent
            embed = discord.Embed(
                description=f"**!Recent Can Be Used to Get the Most Recent 10 IL Runs for a Specific Runner**")
            embed.add_field(name="**!Recent [PLAYER]**",
                            value="ex. !recent *Eleks*: This returns the most recent 10 ILs.", inline=False)
            embed.add_field(name="**!Recent [PLAYER] [CATEGORY]**",
                            value="ex. !recent *Eleks Inbounds*: This returns the most recent 10 ILs in a specific category.",
                            inline=False)
            await message.channel.send(embed=embed)

        elif message[1] == "help":  # !Help
            embed = discord.Embed(description=f"**The help command that you just used.**")
            await message.channel.send(embed=embed)

        else:  # Incorrect Entry
            await message.channel.send(f"No Such Command \"!{message[1]}\" Exists")


def embedProfile(userMessage, profileCreated, playerID, playerName):
    """Creates an embed for the profile command"""

    pName = playerName
    time.sleep(1) # TODO Not sure why you would sleep for 1 sec here?

    if len(userMessage) == 2:

        oPoints = profileCreated[1]
        cat1 = profileCreated[2]
        points1 = profileCreated[4]
        oPlace = profileCreated[0]
        place1 = profileCreated[3]

        embed = discord.Embed(description="")
        if playerID == "":
            embed.set_thumbnail(
                url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.freebiesupply.com%2Flogos%2Flarge%2F2x%2Fportal-9-logo-png-transparent.png&f=1&nofb=1")
            embed.set_author(name=f"{pName}'s Profile:")
        else:
            embed.set_thumbnail(url=f"https://www.speedrun.com/userasset/{playerID}/image?v=3d18eec")
            embed.set_author(name=f"{pName}'s Profile:", url=f"https://www.speedrun.com/user/{playerName}")

        embed.add_field(name=f"**Overall Points:**", value=f"{oPoints}", inline=False)
        embed.add_field(name=f"**{cat1} Points:**", value=f"{points1}", inline=True)

        if len(profileCreated) == 5:

            embed.add_field(name=f"\n**Overall Place:**", value=f"{oPlace}", inline=False)
            embed.add_field(name=f"**{cat1} Place:**", value=f"{place1}", inline=True)
            embed.add_field(name=f"**Top 10 Runs:**", value="** **", inline=False)

        if len(profileCreated) == 8:

            cat2 = profileCreated[5]
            points2 = profileCreated[7]
            place2 = profileCreated[6]

            embed.add_field(name=f"**{cat2} Points:**", value=f"{points2}", inline=True)
            embed.add_field(name=f"\n**Overall Place:**", value=f"{oPlace}", inline=False)
            embed.add_field(name=f"**{cat1} Place:**", value=f"{place1}", inline=True)
            embed.add_field(name=f"**{cat2} Place:**", value=f"{place2}", inline=True)
            embed.add_field(name=f"**Top 10 Runs:**", value="** **", inline=False)

        elif len(profileCreated) == 11:

            cat2 = profileCreated[5]
            points2 = profileCreated[7]
            place2 = profileCreated[6]
            cat3 = profileCreated[8]
            points3 = profileCreated[10]
            place3 = profileCreated[9]

            embed.add_field(name=f"**{cat2} Points:**", value=f"{points2}", inline=True)
            embed.add_field(name=f"**{cat3} Points:**", value=f"{points3}", inline=True)
            embed.add_field(name=f"\n**Overall Place:**", value=f"{oPlace}", inline=False)
            embed.add_field(name=f"**{cat1} Place:**", value=f"{place1}", inline=True)
            embed.add_field(name=f"**{cat2} Place:**", value=f"{place2}", inline=True)
            embed.add_field(name=f"**{cat3} Place:**", value=f"{place3}", inline=True)
            embed.add_field(name=f"**Top 10 Runs:**", value="** **", inline=False)

    elif (len(userMessage) == 3) or (len(userMessage) == 4):
        cat1 = profileCreated[1]
        points = profileCreated[3]
        place = profileCreated[2]

        embed = discord.Embed(description="")
        if playerID == "":
            embed.set_thumbnail(
                url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.freebiesupply.com%2Flogos%2Flarge%2F2x%2Fportal-9-logo-png-transparent.png&f=1&nofb=1")
            embed.set_author(name=f"{pName}'s {cat1} Profile:")
        else:
            embed.set_thumbnail(url=f"https://www.speedrun.com/userasset/{playerID}/image?v=3d18eec")
            embed.set_author(name=f"{pName}'s {cat1} Profile:", url=f"https://www.speedrun.com/user/{playerName}")

        embed.add_field(name=f"**{cat1} Points:**", value=f"{points}", inline=True)
        embed.add_field(name=f"**{cat1} Place:**", value=f"{place}", inline=True)
        if len(userMessage) == 4:
            embed.add_field(name=f"**All Runs:**", value="** **", inline=False)
        else:
            embed.add_field(name=f"**Top 10 Runs:**", value="** **", inline=False)

    return embed


def embedRun(runInfo):
    """Creates an embed for the run command."""

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
    runTicks = (float(time) / .015)

    if vidLink == "N/A":
        embed = discord.Embed(description=f"[Run]({runLink}) | N/A")
    else:
        embed = discord.Embed(description=f"[Run]({runLink}) | [Video]({vidLink})")

    if playerID == "":
        embed.set_thumbnail(
            url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.freebiesupply.com%2Flogos%2Flarge%2F2x%2Fportal-9-logo-png-transparent.png&f=1&nofb=1")
        embed.set_author(name=f"{pName}'s {cat} {chamber} Run")
    else:
        embed.set_thumbnail(url=f"https://www.speedrun.com/userasset/{playerID}/image?v=3d18eec")
        embed.set_author(name=f"{pName}'s {cat} {chamber} Run", url=f"https://www.speedrun.com/user/{pName}")

    # TODO Switch statement instead
    if place == 1:
        embed.add_field(name="**Place**", value=":trophy: 1st", inline=True)
    elif place == 2:
        embed.add_field(name="**Place**", value=":second_place: 2nd", inline=True)
    elif place == 3:
        embed.add_field(name="**Place**", value=":third_place: 3rd", inline=True)
    else:
        embed.add_field(name="**Place**", value=f"{place}th", inline=True)

    embed.add_field(name="**Points**", value=f"{points}", inline=True)
    embed.add_field(name="**Date**", value=f"{date}", inline=False)
    embed.add_field(name="**Time**", value=f"{time}", inline=True)
    embed.add_field(name="**Ticks**", value=f"{runTicks:.0f}", inline=True)

    return embed


client.run(open("botToken.txt", "r").read())
