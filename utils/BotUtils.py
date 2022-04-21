import datetime
import time

import discord

import DBHelper

category_list = ["Inbounds", "Out_of_Bounds", "Glitchless"]
level_list = ["00_01", "02_03", "04_05", "06_07", "08", "09", "10",
              "11_12", "13", "14", "15", "16", "17", "18", "19", "e00", "e01", "e02",
              "Adv_13", "Adv_14", "Adv_15", "Adv_16", "Adv_17", "Adv_18"]


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


def input_to_chamber(chamber):
    """Takes input and converts it to correctly formatted chamber name"""
    chamber = chamber.replace('/', '')
    chamber = chamber.replace('-', '')

    if chamber == '10':
        return level_list[6]  # 10
    else:
        userChamber = chamber.replace('0', '')

    if 'adv' in userChamber:
        chamber = userChamber.replace('anced', '')

        if chamber == 'adv13':
            return level_list[18]  # adv13
        elif chamber == 'adv14':
            return level_list[19]  # adv14
        elif chamber == 'adv15':
            return level_list[20]  # adv15
        elif chamber == 'adv16':
            return level_list[21]  # adv16
        elif chamber == 'adv17':
            return level_list[22]  # adv17
        elif chamber == 'adv18':
            return level_list[23]  # adv18
        else:
            return ''

    elif 'e' in chamber:
        if chamber == 'e':
            return level_list[15]  # e00
        elif chamber == 'e1':
            return level_list[16]  # e01
        elif chamber == 'e2':
            return level_list[17]  # e02
        else:
            return ''

    else:
        if userChamber == '' or userChamber == '1' or userChamber.lower() == "owo":
            return level_list[0]  # 00-01
        elif userChamber == '23' or userChamber == '2' or userChamber == '3':
            return level_list[1]  # 02-03
        elif userChamber == '45' or userChamber == '4' or userChamber == '5':
            return level_list[2]  # 04-05
        elif userChamber == '67' or userChamber == '6' or userChamber == '7':
            return level_list[3]  # 06-07
        elif userChamber == '8':
            return level_list[4]  # 08
        elif userChamber == '9':
            return level_list[5]  # 09
        elif userChamber == '1112' or userChamber == '11' or userChamber == '12':
            return level_list[7]  # 11-12
        elif userChamber == '13':
            return level_list[8]  # 13
        elif userChamber == '14':
            return level_list[9]  # 14
        elif userChamber == '15':
            return level_list[10]  # 15
        elif userChamber == '16':
            return level_list[11]  # 16
        elif userChamber == '17':
            return level_list[12]  # 17
        elif userChamber == '18':
            return level_list[13]  # 18
        elif userChamber == '19':
            return level_list[14]  # 19
        elif userChamber == '10':
            pass
        else:
            return ''


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


def convert_to_ticks(input_str):
    minutes = ''
    seconds = ''
    millis = ''
    time_override = input_str.replace(':', '#').replace('.', '#')
    time_split = time_override.split('#')

    if len(time_split) == 2:
        minutes = 0
        seconds = int(time_split[0])
        millis = int(time_split[1])

    if len(time_split) == 3:
        minutes = int(time_split[0])
        seconds = int(time_split[1])
        millis = int(time_split[2])

    ticks = ((minutes * 60000) + (seconds * 1000) + millis) / 15

    return ticks


def convert_to_human_time(input_ticks):
    ms = int(input_ticks) * 15
    seconds, ms = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    return f'{int(minutes):02d}:{int(seconds):02d}.{int(ms):03d}'
