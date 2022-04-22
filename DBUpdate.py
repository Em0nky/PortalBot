#Imports
import sqlite3
import pandas
from sqlite3 import Error

dataGrabbed = True

try:
    exec(open('DBDataGrab.py').read())
except:
    print("API Failed Somehow, Run it again.")
    dataGrabbed = False

if dataGrabbed:
    #Variables
    file = "PointsDB.db"

    catList = ["Inbounds", "Out_of_Bounds", "Glitchless"]

    chamberList = ["00_01", "02_03", "04_05", "06_07", "08", "09", "10", 
                "11_12", "13", "14", "15", "16", "17", "18", "19", "e00", "e01", "e02",
                "Adv_13", "Adv_14", "Adv_15", "Adv_16", "Adv_17", "Adv_18"]

    #Database Creation
    conn = None
    try:
        conn = sqlite3.connect(file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    #Cursor Object
    cursor = conn.cursor()

    #Population and Creation of Tables
    df = pandas.read_csv('userList.csv') #Makes the CSV of Runners into a dataframe

    df.to_sql('runners', conn, if_exists='replace', index=True) #Creates a table based on CSV

    df = pandas.read_csv('runList.csv') #Make the CSV of Runs into a Dataframe
    df = df.replace('-', '_', regex=True) #Replaces - in Chambers with _
    df = df.replace(' ', '_', regex=True) #Replaces spaces in all data with _
    df.to_sql('runs', conn, if_exists='replace', index=True) #Creates a table based on Dataframe


    #Creation of Views

    #View for each individual level board
    for cat in catList:
        for chamber in chamberList:
            conn.execute(f"""
            DROP VIEW IF EXISTS {cat}_{chamber};""")

            conn.execute(f"""
            CREATE VIEW {cat}_{chamber} AS
            SELECT Category, Chamber, Place, RunnerName, SRCID, Time, Ticks, Points, Date, Link, VideoLink
            FROM runs
            WHERE Category = "{cat}" AND Chamber = "{chamber}";
            """)

            print(f"""{cat}_{chamber}""")

    #View for runs of each category
    for cat in catList:
        conn.execute(f"""
        DROP VIEW IF EXISTS {cat}_Runs;""")

        conn.execute(f"""
        CREATE VIEW {cat}_Runs AS
        SELECT Category, Chamber, Place, RunnerName, SRCID, Time, Ticks, Points, Date, Link, VideoLink
        FROM runs
        WHERE Category = "{cat}";
        """)

    #View for each category points
    for cat in catList:
        conn.execute(f"""
        DROP VIEW IF EXISTS {cat}_Runner_Board;""")

        conn.execute(f"""
        CREATE VIEW {cat}_Runner_Board AS
        SELECT RunnerName, SRCID, SUM(Points)
        FROM {cat}_Runs
        WHERE Category = "{cat}"
        GROUP BY RunnerName
        ORDER BY SUM(Points) DESC;
        """)

    #All Cats Points List View
    conn.execute(f"""
    DROP VIEW IF EXISTS Overall_Runner_Board;""")

    conn.execute(f"""
    CREATE VIEW Overall_Runner_Board AS
    SELECT RunnerName, SRCID, SUM(Points)
    FROM runs
    GROUP BY RunnerName
    ORDER BY SUM(Points) DESC;
    """)


    #Creation of Scripts

    #Debug Viewing tables and views
    for row in cursor.execute('SELECT * FROM runs;'):
        print(row)

    for row in cursor.execute('SELECT * FROM runners;'):
        print(row)

    for row in cursor.execute('SELECT * FROM Inbounds_02_03;'):
        print(row)

    for row in cursor.execute('SELECT * FROM Inbounds_Runs;'):
        print(row)

    for row in cursor.execute('SELECT * FROM Overall_Runner_Board;'):
        print(row)

    conn.close() #Close database
