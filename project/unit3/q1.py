#cmput 391 proj #3 team20
#q1 
import sys
import csv
import sqlite3

#connet to database
conn = sqlite3.connect('edmonton.db')
cur = conn.cursor()
#turn on foreign key verification
cur.execute('PRAGMA foreign_keys = ON;')

#Read from command shell
sql_file = sys.argv[1]

#Find min values for lat and lon
origin = cur.execute("SELECT MIN(lat), MIN(lon) FROM node;")
min_lat, min_lon = origin.fetchone()

#stdout
print ".open edmonton.db"
print ".read %s" % sql_file
print "CREATE TABLE IF NOT EXISTS nodeCartesian (id INTEGER PRIMARY KEY, x FLOAT, y FLOAT);"
print "INSERT INTO nodeCartesian (id, x, y) SELECT id, ( (lat - %s ) * 111286), ( (lon - %s) * 67137 ) FROM node; " % (min_lat, min_lon)
                    
#close db
conn.commit()
conn.close()

