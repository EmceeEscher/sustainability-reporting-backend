import psycopg2

def connectAndRun(funcToRun):
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost", database="sustainabilitytest", user="postgres", password="SuperUser100")

        # create a cursor
        cur = conn.cursor()

        # pass the cursor to the function so it can execute
        funcToRun(cur)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def addUser(username, unit, adminLevel):
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost", database="sustainabilitytest", user="postgres", password="SuperUser100")

        # create a cursor
        cur = conn.cursor()

        print("username: " + username)
        print("unit: " + unit)
        print("adminLevel: " + adminLevel)
        command = ("""
            INSERT INTO users (username, unit, admin_level) 
            VALUES (%s, %s, %s)
        """, [username, unit, adminLevel])

        cur.execute(command[0], command[1])


        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')