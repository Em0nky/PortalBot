from dto.RunDTO import RunDTO
import mysql.connector

from dto.RunnerDTO import RunnerDTO

connection = None


def get_connection():
    global connection
    if connection is None:
        connection = mysql.connector.connect(host='localhost', database='portal_ils', user='root')
    return connection


def get_all_runs():
    c = get_connection().cursor()
    c.execute('select * from runs')
    result = c.fetchall()
    runs = list()

    for x in result:
        dto = RunDTO(
            category=x[0],
            speedrun_username=x[1],
            speedrun_id=x[2],
            level=x[3],
            weblink=x[4],
            video=x[5],
            demos=x[6],
            place=x[7],
            points=x[8],
            time=x[9],
            date=x[10]
        )

        runs.append(dto)

    return reversed(list(runs))


def get_all_runners():
    c = get_connection().cursor()
    c.execute('select * from runners')
    result = c.fetchall()
    runners = []

    for x in result:
        dto = RunnerDTO(
            discord_id=x[0],
            speedrun_username=x[1],
            speedrun_id=x[2],
            rank_overall=x[3],
            rank_inbounds=x[4],
            rank_oob=x[5],
            rank_glitchless=x[6],
            points_overall=x[7],
            points_inbounds=x[8],
            points_oob=x[9],
            points_glitchless=x[10]
        )

        runners.append(dto)

    return runners


def add_discord_id_to_runner(discord_id, speedrun_username):

    c = get_connection().cursor()
    c.execute(f'update runners set discord_id={discord_id} where speedrun_username="{speedrun_username}"')
