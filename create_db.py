import sqlite3 as lite
import sys
con = lite.connect('sensehat.db')
with con: 
    cur = con.cursor() 
    cur.execute("DROP TABLE IF EXISTS SENSEHAT_data")
    cur.execute("CREATE TABLE SENSEHAT_data(id INTEGER PRIMARY KEY AUTOINCREMENT, recorded_time DATETIME, temp NUMERIC, humidity NUMERIC)")