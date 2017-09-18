import psycopg2
import psycopg2.extras
from .models.user import User
from .models.unit import Unit
from .exceptions.dbException import DbException

def connectAndRun(commands):
    conn = None
    result = 'OK'
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost", database="sustainabilitytest", user="postgres", password="SuperUser100")

        # create a cursor
        cur = conn.cursor()

        for command in commands:
            cur.execute(command[0], command[1])

        # close the communication with the PostgreSQL
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        result = error.pgerror
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
        return result

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

def initializeTables():
    commands = []
    commands.append(("""
        CREATE TABLE users (
          user_id integer PRIMARY KEY,
          username text NOT NULL,
          admin_level admin_level NOT NULL
        )
        """, []))
    commands.append(("""
        CREATE TABLE units (
          unit_id serial PRIMARY KEY,
          name text NOT NULL,
          description text,
          admin_id integer REFERENCES users (user_id)
        )
    """, []))
    commands.append(("""
        ALTER TABLE users ADD unit_id integer REFERENCES units (unit_id)
    """, []))
    return connectAndRun(commands)

def initializeTypes():
    commands = []
    commands.append(("""
        CREATE TYPE admin_level AS ENUM ('user', 'admin', 'superadmin')
        """, []))
    return connectAndRun(commands)

# Cleanup functions (primarily for use in testing and development, don't use on live database)

def deleteTables():
    commands = []
    commands.append(("""
        DROP TABLE users CASCADE
    """, []))
    commands.append(("""
        DROP TABLE units CASCADE
    """, []))
    return connectAndRun(commands)

# User functions

def addUser(userId, username, unit, adminLevel):
    commands = []
    commands.append(("""
            INSERT INTO users (user_id, username, unit_id, admin_level) 
            VALUES (%s, %s, %s, %s)
        """, [userId, username, unit, adminLevel]))
    return connectAndRun(commands)

def getUsers():
    commands = []
    commands.append(("""
        SELECT * FROM users
    """, []))
    data = connectAndRetrieve(commands)
    users = []
    for row in data:
        users.append(User(row["username"], row["unit_id"], row["admin_level"]))
    return users

def getUser(userId):
    commands = []
    commands.append(("""
        SELECT * FROM users 
        WHERE user_id = %s
    """, userId))
    data = connectAndRetrieve(commands)
    if len(data) == 0:
        raise DbException("No entry found")
    userData = data[0]
    user = User(userData["username"], userData["unit_id"], userData["admin_level"])
    return user

def addUserToUnit(userId, unitId):
    commands = []
    commands.append(("""
        UPDATE users SET unit_id = %s WHERE user_id = %s
    """, [unitId, userId]))
    return connectAndRun(commands)

# Unit functions

def addUnit(name, description, adminId):
    commands = []
    commands.append(("""
        INSERT INTO units (name, description, admin_id)
        VALUES (%s, %s, %s)
    """, [name, description, adminId]))
    return connectAndRun(commands)

def getUnits():
    commands = []
    commands.append(("""
        SELECT * FROM units
    """, []))
    data = connectAndRetrieve(commands)
    units = []
    for row in data:
        units.append(Unit(row["name"], row["description"], row["admin_id"]))
    return units