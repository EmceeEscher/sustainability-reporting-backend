import psycopg2

def connectAndRun(commands):
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost", database="sustainabilitytest", user="postgres", password="SuperUser100")

        # create a cursor
        cur = conn.cursor()

        for command in commands:
            cur.execute(command[0], command[1])
            print("command[0]: " + command[0])

        # close the communication with the PostgreSQL
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def connectAndRetrieve(commands):
    conn = None
    data = ''
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost", database="sustainabilitytest", user="postgres", password="SuperUser100")

        # create a cursor
        cur = conn.cursor()

        for command in commands:
            cur.execute(command[0], command[1])
            print("command[0]: " + command[0])

        data = cur.fetchall()
        # close the communication with the PostgreSQL
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
        return data

def addUser(username, unit, adminLevel):

    commands = []
    commands.append(("""
            INSERT INTO users (username, unit, admin_level) 
            VALUES (%s, %s, %s)
        """, [username, unit, adminLevel]))
    connectAndRun(commands)

def initializeTable():
    commands = []
    commands.append(("""
        CREATE TABLE users (
          user_id SERIAL PRIMARY KEY,
          username TEXT NOT NULL,
          unit unit,
          admin_level admin_level NOT NULL
        )
        """, []))
    connectAndRun(commands)

def initializeTypes():
    commands = []
    commands.append(("""
        CREATE TYPE admin_level AS ENUM ('user', 'admin', 'superadmin')
        """, []))
    commands.append(("""
        CREATE TYPE unit AS ENUM ('exampleUnit1', 'exampleUnit2')
        """, []))
    connectAndRun(commands)

def getUsers():

    commands = []
    commands.append(("""
        SELECT * FROM users
    """, []))
    data = connectAndRetrieve(commands)
    for object in data:
        print(object)
    return 'OK'

def deleteTables():

    commands = []
    commands.append(("""
        DROP TABLE users
    """, []))
    connectAndRun(commands)
