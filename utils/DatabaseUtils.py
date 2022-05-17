from mysql.connector import MySQLConnection
from dto.RunDTO import RunDTO
import mysql.connector
from dto.RunnerDTO import RunnerDTO

connection = None


def get_connection() -> MySQLConnection:

    global connection
    if connection is None:
        # TODO Use config values
        connection = mysql.connector.connect(host='localhost', database='portal_ils', user='root')
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


def add_discord_id_to_runner(discord_id: int, speedrun_username: str):

    c = get_connection().cursor()
    c.execute(f'update runners set discord_id={discord_id} where speedrun_username="{speedrun_username}"')
