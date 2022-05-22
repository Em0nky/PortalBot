from typing import Any

from mysql.connector import MySQLConnection
from dto.RunDTO import RunDTO
import mysql.connector
from dto.RunnerDTO import RunnerDTO

connection = None


def get_connection() -> MySQLConnection:

    global connection
    if connection is None:
        connection = mysql.connector.connect(host='localhost', database='portal_ils', user='root')
        # Allow for better error handling
        # connection.get_warnings = True
        # connection.raise_on_warnings = True
    return connection


def get_all_runs() -> list:

    c = get_connection().cursor()
    c.execute('select * from runs')
    results = c.fetchall()
    runs = list()

    for result in results:
        dto = RunDTO(
            category=result[0],
            speedrun_username=result[1],
            speedrun_id=result[2],
            level=result[3],
            weblink=result[4],
            video=result[5],
            demos=result[6],
            place=result[7],
            points=result[8],
            time=result[9],
            date=result[10]
        )

        runs.append(dto)

    return runs


def get_runner_from_name(speedrun_username: str) -> RunnerDTO:

    c = get_connection().cursor()
    c.execute('select * from runners where speedrun_username="%s"' % speedrun_username)
    result = c.fetchone()

    return RunnerDTO(
        discord_id=result[0],
        speedrun_username=result[1],
        speedrun_id=result[2],
        rank_overall=result[3],
        rank_inbounds=result[4],
        rank_oob=result[5],
        rank_glitchless=result[6],
        points_overall=result[7],
        points_inbounds=result[8],
        points_oob=result[9],
        points_glitchless=result[10]
    )


def get_runner_from_discord_id(discord_id: int) -> RunnerDTO:

    c = get_connection().cursor()
    c.execute('select * from runners where discord_id=%s' % discord_id)
    result = c.fetchone()

    return RunnerDTO(
        discord_id=result[0],
        speedrun_username=result[1],
        speedrun_id=result[2],
        rank_overall=result[3],
        rank_inbounds=result[4],
        rank_oob=result[5],
        rank_glitchless=result[6],
        points_overall=result[7],
        points_inbounds=result[8],
        points_oob=result[9],
        points_glitchless=result[10]
    )


def get_all_runs_from_player(player: str) -> list:

    c = get_connection().cursor()
    c.execute('select * from runs where speedrun_username="%s"' % player)
    results = c.fetchall()
    all_runs = list()

    for r in results:
        r = RunDTO(
            category=r[0],
            speedrun_username=r[1],
            speedrun_id=r[2],
            level=r[3],
            weblink=r[4],
            video=r[5],
            demos=r[6],
            place=r[7],
            points=r[8],
            time=r[9],
            date=r[10]
        )
        all_runs.append(r)

    return all_runs


def get_run_from_player(player: str, category: str, level: str) -> RunDTO:

    c = get_connection().cursor()
    c.execute('select * from runs where speedrun_username="%s" and level="%s" and category="%s"' % (player, level, category))
    result = c.fetchone()

    return RunDTO(
        category=result[0],
        speedrun_username=result[1],
        speedrun_id=result[2],
        level=result[3],
        weblink=result[4],
        video=result[5],
        demos=result[6],
        place=result[7],
        points=result[8],
        time=result[9],
        date=result[10]
    )


def get_all_runners() -> list:

    c = get_connection().cursor()
    c.execute('select * from runners')
    results = c.fetchall()
    runners = list()

    for result in results:
        dto = RunnerDTO(
            discord_id=result[0],
            speedrun_username=result[1],
            speedrun_id=result[2],
            rank_overall=result[3],
            rank_inbounds=result[4],
            rank_oob=result[5],
            rank_glitchless=result[6],
            points_overall=result[7],
            points_inbounds=result[8],
            points_oob=result[9],
            points_glitchless=result[10]
        )

        runners.append(dto)

    return runners


def add_or_update_discord_id_of_runner(speedrun_username: str, discord_id: int):

    c = get_connection().cursor()
    c.execute(f'select speedrun_username, discord_id from runners where discord_id=%d' % discord_id)
    result = c.fetchall()

    # If query returns nothing, this username has not been registered, yet
    # Therefore we will add the discord_id to that runner
    if len(result) == 0:
        c.execute(f'update runners set discord_id=%d where speedrun_username="%s"' % (discord_id, speedrun_username))
        get_connection().commit()
        return

    # In case a user has already connected their account
    # Fetch their old username
    c.execute('select speedrun_username from runners where discord_id=%d' % discord_id)
    old_username = c.fetchone()

    # Set discord_id to 0 for the old user, effectively disconnecting it
    c.execute('update runners set discord_id=0 where speedrun_username="%s"' % old_username)

    # Update discord_id for new username
    c.execute('update runners set discord_id=%d where speedrun_username="%s"' % (discord_id, speedrun_username))
    get_connection().commit()
