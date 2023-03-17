import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

## POSTGRESQL config vars
DATABASE = config["POSTGRESQL"]["DATABASE"]
HOST = config["POSTGRESQL"]["HOST"]
USER = config["POSTGRESQL"]["USER"]
PORT = config["POSTGRESQL"]["PORT"]

conn = psycopg2.connect(database=DATABASE,
                        host=HOST,
                        user=USER, 
                        password="",
                        port=PORT)

cur = conn.cursor()
cur.execute("SELECT * FROM tag")

rows = cur.fetchall()
for r in rows:
    print(f"{r[0]} - {r[1]}")

cur.close()
conn.close()
