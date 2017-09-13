import psycopg2
import psycopg2.extras
from .models.user import User

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
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

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

# Initialization functions

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

# Cleanup functions (primarily for use in testing and development, don't use on live database)

def deleteTables():
    commands = []
    commands.append(("""
        DROP TABLE users
    """, []))
    connectAndRun(commands)

# User functions

def addUser(username, unit, adminLevel):

    commands = []
    commands.append(("""
            INSERT INTO users (username, unit, admin_level) 
            VALUES (%s, %s, %s)
        """, [username, unit, adminLevel]))
    connectAndRun(commands)

def getUsers():
    commands = []
    commands.append(("""
        SELECT * FROM users
    """, []))
    data = connectAndRetrieve(commands)
    users = []
    for row in data:
        users.append(User(row["username"], row["unit"], row["admin_level"]))
    return users

def getUser(userId):
    commands = []
    commands.append(("""
        SELECT * FROM users 
        WHERE user_id = %s
    """, userId))
    data = connectAndRetrieve(commands)
    userData = data[0]
    user = User(userData["username"], userData["unit"], userData["admin_level"])
    return user

