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
            await message.channel.send(boardCreated)
            await message.channel.send(file=discord.File('list.png'))
            '''
            validPageList = False
            if(len(userMessage) == 1 or (len(userMessage) == 2 and not(userMessage[1].isnumeric()))):
                validPageList = True
            
            if (validPageList == True):
                #Reaction Stuff
                currentHighestPlayer = 20
                catList = PP.createAllCatPointsList()
                maxPlayers = len(catList)
                reactionTimeout = 0
                while(reactionTimeout == 0):
                    await message.add_reaction("⬅️")
                    await message.add_reaction("➡️")

                    def check (reaction, user):
                        return user == message.author and str(reaction.emoji) in ['⬅️','➡️']
                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=15.0, check=check)

                        if(reaction.emoji == '⬅️' and currentHighestPlayer == 10):
                            await message.channel.send('Cannot Go Below Top 10 Players.')

                        elif(reaction.emoji == '⬅️' and currentHighestPlayer > 10):
                            #Edit previous message w/ new image of previous 10 players
                            await message.delete()
                            boardCreated = PP.leaderboardArrowCommand(userMessage, currentHighestPlayer)
                            await message.channel.send(file=discord.File('list.png'))
                            currentHighestPlayer = currentHighestPlayer - 10

                        elif(reaction.emoji == '➡️' and currentHighestPlayer > maxPlayers - 10):
                            await message.channel.send('Cannot Go Past End of Leaderboard.')

                        elif(reaction.emoji == '➡️' and currentHighestPlayer <= maxPlayers - 10):
                            #Edit previous message w/ new image of next 10 players
                            await message.delete()
                            boardCreated = PP.leaderboardArrowCommand(userMessage, currentHighestPlayer)
                            await message.channel.send(file=discord.File('list.png'))
                            currentHighestPlayer = currentHighestPlayer + 10

                    except asyncio.TimeoutError:
                        reactionTimeout = 1
                        for r in message.reactions:
                            await message.clear_reaction(r)
                    except:
                        reactionTimeout = 1
                        for r in message.reactions:
                            await message.clear_reaction(r) '''


        elif (boardCreated == "lengthfail"): #Fail
            await message.channel.send('Invalid Leaderboard Length.')

        elif (boardCreated == "modfail"): #Fail
            await message.channel.send('Invalid Leaderboard Modifier. !help lb')

        else: #Fail
            await message.channel.send('Something went wrong')
            

    #Chamber Points Leaderboard Commands
    if message.content.startswith('!Levelboard') or message.content.startswith('!lvlb') or\
        message.content.startswith('!levelboard'):

        userMessage = message.content.split(" ")

        try:
            boardCreated = PP.levelboardCommand(userMessage)
        except:
            await message.channel.send('Invalid Leaderboard Command.')
        
        if ("Glitchless" in boardCreated or "Out of Bounds" in boardCreated or "Inbounds" in boardCreated): #Success
            await message.channel.send(boardCreated)
            await message.channel.send(file=discord.File('list.png'))

        elif (boardCreated == "chamberfail"): #Fail
            await message.channel.send('Invalid Chamber. !help lb')

        elif (boardCreated == "catfail"): #Fail
            await message.channel.send('Invalid Category. !help lb')

        else: #Fail
            await message.channel.send('Invalid Command.')


    if message.content.startswith('!profile') or message.content.startswith('!pf') or\
        message.content.startswith('!Profile') or message.content.startswith('!Pf'):

        userMessage = message.content.split(" ")
        
        try:
            profileCreated = PP.userprofileCommand(userMessage)
        except:
            await message.channel.send('Invalid Profile Command.')
        
        

        if (len(profileCreated) > 8):
            profileCreated = profileCreated.split(",")
            if(len(userMessage) == 2): #Default

                if (len(profileCreated) == 5):
                    await message.channel.send(f"**{userMessage[1]}'s Profile:**\nOverall Points: **{profileCreated[1]}**  **|**  {profileCreated[2]} Points: **{profileCreated[4]}** " +
                    f"\nOverall Place: **{profileCreated[0]}**  **|**  {profileCreated[2]} Place: **{profileCreated[3]}**" +
                    f"\n**Top 5 Scores:**")

                elif(len(profileCreated) == 8):
                    await message.channel.send(f"**{userMessage[1]}'s Profile:**\nOverall Points: **{profileCreated[1]}**  **|**  {profileCreated[2]} Points: **{profileCreated[4]}**  **|**  " + 
                    f"{profileCreated[5]} Points: **{profileCreated[7]}** " + 
                    f"\nOverall Place: **{profileCreated[0]}**  **|**  {profileCreated[2]} Place: **{profileCreated[3]}**  **|** {profileCreated[5]} Place: **{profileCreated[6]}**" +
                    f"\n**Top 5 Scores:**")

                elif(len(profileCreated) == 11):
                    await message.channel.send(f"**{userMessage[1]}'s Profile:**\nOverall Points: **{profileCreated[1]}**  **|**  {profileCreated[2]} Points: **{profileCreated[4]}**  **|**  " + 
                    f"\n{profileCreated[5]} Points: **{profileCreated[7]}**  **|**  {profileCreated[8]} Points: **{profileCreated[10]}** " + 
                    f"\nOverall Place: **{profileCreated[0]}**  **|**  {profileCreated[2]} Place: **{profileCreated[3]}**   \n{profileCreated[5]} Place: **{profileCreated[6]}**  **|**  " + 
                    f"{profileCreated[8]} Place: **{profileCreated[9]}**" +
                    f"\n**Top 5 Scores:**")


            elif(len(userMessage) == 3): #Category
                await message.channel.send(f"**{userMessage[1]}'s {profileCreated[1]} Profile:**\n{profileCreated[1]} Points: **{profileCreated[3]}**  **|**  {profileCreated[1]} Place: **{profileCreated[2]}**")

            elif(len(userMessage) == 4): #Category All
                await message.channel.send(f"**All of {userMessage[1]}'s {profileCreated[1]} Runs:**\n{profileCreated[1]} Points: **{profileCreated[3]}**  **|**  {profileCreated[1]} Place: **{profileCreated[2]}**")

            await message.channel.send(file=discord.File('list.png'))

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



    #Help Command
    if (message.content).lower() == ('!help'):
        await message.channel.send('''**List of Commands for PortalBot:**\n
        **Leaderboards: **!Leaderboard [*optional*] [*optional*] [*optional*]\n
        **Levelboards: **!Levelboard [*category*] [*level*]\n
        **User Profile: **!Profile [*player name*] [*optional*] [*optional*]\n
        **For Help with Specific Commands Enter \"!help [command]\"** ex. \"!help *leaderboard*\"''')
    

    #Specific Help Commands
    if message.content.startswith('!help '):
        userMessage = (message.content.lower()).split(" ")

        if (userMessage[1] == "leaderboard") or (userMessage[1] == "lb"): #!Leaderboard
            await message.channel.send('''**!Leaderboard (or !lb) Can Be Used to Get an Image of a Particular Point Leaderboard**\n
        **\"!Leaderboard\" (Default Command):** This returns an overall points leaderboard of the top 10 runners.\n
        **\"!Leaderboard Max\":** This returns an overall points leaderboard of all runners. (This is really tall)\n
        **\"!Leaderboard [NUMBER]\"** | ex. \"!lb *15*\": This returns an overall points leaderboard of the top [NUMBER] runners.\n
        **\"!Leaderboard [CATEGORY]\"** | ex. \"!lb *inbounds*\": This returns a points leaderboard for the specified category of the top 10 runners.\n
        **\"!Leaderboard [CATEGORY] [NUMBER]\"** | ex. \"!lb *inbounds 25*\": This returns a points leaderboard for the specified category of the top [NUMBER] runners.\n
    **Instructions on leaderboards of runs for a specific chamber can be found with \"!help levelboard\".**''')

        elif (userMessage[1] == "levelboard") or (userMessage[1] == "lvlb"): #!Levelboard
            await message.channel.send('''**!Levelboard (or !lvlb) Can Be Used to Get an Image of a Particular Level's Point Leaderboard**\n
        **\"!Levelboard [CATEGORY] [LEVEL]\"** | ex. \"!lvlb *inbounds 00/01*\": This returns an overall points leaderboard of the top 10 runners.''')

        elif (userMessage[1] == "profile"): #!Profile
            await message.channel.send('''**!Profile Can Be Used to Get Different Information or Lists for a Specific Runner**\n
        **\"!Profile\" (Default Command):** This returns a linked user's top 5 runs and total points. **NOT IMPLEMENTED**\n
        **\"!Profile [PLAYER]\"** | ex. \"!Profile *Shizzal*\": This returns the user's top 5 runs, overall place w/ total points, and place w/ points for each cat.\n
        **\"!Profile [PLAYER] [CATEGORY]\"** | ex. \"!Profile *Shizzal* *Inbounds*\": This returns the user's top 10 runs from the category, overall place in the cat and points.\n
        **\"!Profile [PLAYER] [CATEGORY] All\"** | ex. \"!Profile *Shizzal* *Inbounds* All\": This returns all the user's runs from the category, overall place in the cat and points.\n
        
        **NOT CURRENTLY IMPLEMENTED**''')

        else: #Incorrect Entry
            await message.channel.send(f"No Such Command \"!{userMessage[1]}\" Exists")



tokenFile = open("botToken.txt", "r")

client.run(tokenFile.read())
