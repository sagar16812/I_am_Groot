import sqlite3 as lite
import sys

con = lite.connect('sensorsData.db')

with con:

    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS sms_data")
    cur.execute("CREATE TABLE sms_data(id INTEGER PRIMARY KEY AUTOINCREMENT , readtime DATETIME NOT NULL, username TEXT NOT NULL, soilmoisture TEXT NOT NULL,temp TEXT NOT NULL, press TEXT NOT NULL, hum TEXT NOT NULL, status TEXT NOT NULL)")
con.close()
