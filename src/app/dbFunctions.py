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
        CREATE TABLE units (
          unit_id serial PRIMARY KEY,
          name text NOT NULL,
          description text
        )
    """, []))
    commands.append(("""
        CREATE TABLE users (
          user_id integer PRIMARY KEY,
          username text NOT NULL,
          admin_level admin_level NOT NULL,
          unit_id integer REFERENCES units (unit_id)
        )
        """, []))
    commands.append(("""
        CREATE TABLE  unit_admins (
          admin_id integer REFERENCES users (user_id),
          unit_id integer REFERENCES units (unit_id),
          PRIMARY KEY(admin_id, unit_id)
        )
    """, []))
    commands.append(("""
        CREATE TABLE actions (
          action_id serial PRIMARY KEY,
          name text NOT NULL,
          description text NOT NULL,
          stakeholder integer REFERENCES users (user_id),
          theme theme NOT NULL,
          priority_area priority_area NOT NULL
        )
    """, []))
    return connectAndRun(commands)

# only used for testing, so I don't have to delete and create new tables all the time
def initializeNewTables():
    commands = []
    commands.append(("""
        CREATE TABLE actions (
          action_id serial PRIMARY KEY,
          name text NOT NULL,
          description text NOT NULL,
          stakeholder integer REFERENCES users (user_id) NOT NULL,
          theme theme NOT NULL,
          priority_area priority_area NOT NULL
        )
    """, []))
    return connectAndRun(commands)

def initializeTypes():
    commands = []
    commands.append(("""
        CREATE TYPE admin_level AS ENUM ('user', 'admin', 'superadmin')
        """, []))
    commands.append(("""
        CREATE TYPE theme AS ENUM ('Energy & Emissions', 'Materials & Waste', 'Water', 'Purchasing', 'Engagement Programs',
        'Campus as a Living Laboratory')
    """, []))
    commands.append(("""
        CREATE TYPE priority_area AS ENUM ('examplePriorityArea')
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
    commands.append(("""
        DROP TABLE unit_admins CASCADE
    """, []))
    commands.append(("""
        DROP TABLE actions CASCADE
    """, []))
    return connectAndRun(commands)

def deleteTypes():
    commands = []
    commands.append(("""
        DROP TYPE admin_level CASCADE
    """, []))
    commands.append(("""
        DROP TYPE theme CASCADE
    """, []))
    commands.append(("""
        DROP TYPE priority_area CASCADE
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

def addUnit(name, description):
    commands = []
    commands.append(("""
        INSERT INTO units (name, description)
        VALUES (%s, %s)
    """, [name, description]))
    return connectAndRun(commands)

def getUnits():
    commands = []
    commands.append(("""
        SELECT * FROM units
    """, []))
    data = connectAndRetrieve(commands)
    units = []
    for row in data:
        units.append(Unit(row["name"], row["description"]))
    return units

def addUnitAdmin(unitId, adminId):
    commands = []
    commands.append(("""
        INSERT INTO unit_admins (admin_id, unit_id)
        VALUES (%s, %s)
    """, [adminId, unitId]))
    commands.append(("""
        UPDATE users 
        SET admin_level = 'admin' 
        WHERE user_id = %s AND admin_level != 'superadmin' AND admin_level != 'admin'
    """, adminId))
    return connectAndRun(commands)