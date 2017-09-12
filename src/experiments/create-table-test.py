import psycopg2

def create_table():
    commands = (
        """
        CREATE TYPE admin_level AS ENUM ('user', 'admin', 'superadmin')
        """,
        """
        CREATE TYPE unit AS ENUM ('exampleUnit1', 'exampleUnit2')
        """,
        """
        CREATE TABLE users (
          user_id SERIAL PRIMARY KEY,
          username TEXT NOT NULL,
          unit TEXT,
          admin_level TEXT NOT NULL
        )
        """
    )

    conn = None

    try:
        conn = psycopg2.connect(host="localhost", database="sustainabilitytest", user="postgres", password="SuperUser100")
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_table()