import time

import discord


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


def embedProfile(userMessage, profileCreated, playerID, playerName):
    """Creates an embed for the profile command"""

    pName = playerName
    time.sleep(1)
    embed = discord.Embed()

    if len(userMessage) == 1:

        oPoints = profileCreated[1]
        cat1 = profileCreated[2]
        points1 = profileCreated[4]
        oPlace = profileCreated[0]
        place1 = profileCreated[3]

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

    elif len(userMessage) == 2 or len(userMessage) == 3:
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
        if len(userMessage) == 3:
            embed.add_field(name=f"**All Runs:**", value="** **", inline=False)
        else:
            embed.add_field(name=f"**Top 10 Runs:**", value="** **", inline=False)

    return embed
