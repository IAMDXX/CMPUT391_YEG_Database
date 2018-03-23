#cmput 391 proj #3 team20
#q2
import sys
import csv
import sqlite3
import math

#connet to database
conn = sqlite3.connect('edmonton.db')
cur = conn.cursor()
#turn on foreign key verification
cur.execute('PRAGMA foreign_keys = ON;')

#Read from command shell
sql_file = sys.argv[1]

#Read sqlfile
print ".open edmonton.db"
print ".read %s" % sql_file

#create table
print "CREATE TABLE IF NOT EXISTS areaMBR(id INTEGER PRIMARY KEY, minX FLOAT, maxX FLOAT, minY FLOAT, maxY FLOAT);"
print '''
        INSERT INTO areaMBR(id, minX, maxX, minY, maxY)
        SELECT w.id, MIN(nc.x), MAX(nc.x), MIN(nc.y), MAX(nc.y) 
        FROM way w, waypoint wp, nodeCartesian nc
        WHERE w.closed = 1 AND w.id = wp.wayid AND wp.nodeid = nc.id 
        GROUP BY w.id;
        '''
#close db
conn.commit()
conn.close()
