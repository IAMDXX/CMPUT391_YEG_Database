#cmput 391 proj #3 team20
#q1 
import sys
import csv
import sqlite3
import math

#connet to database
conn = sqlite3.connect('q1.db')
cur = conn.cursor()
#turn on foreign key verification
cur.execute('PRAGMA foreign_keys = ON;')

#Read from command shell
sql_file = sys.argv[1]

#Read sqlfile
f = open(sql_file,'r')
sql_File = f.read()
f.close()
qry = sql_File.split(';')
for command in qry:
    cur.execute(command)

node_id_list = []
node_lat =[]
node_lon =[]
                    
#read all nodes from node table
nodes = cur.execute("SELECT * FROM node;")
for n in nodes:
    n=list(n)
    node_id_list.append(str(n[0]))
    node_lat.append(n[1])
    node_lon.append(n[2])
#find min_lat and min_lon
origin = cur.execute("SELECT MIN(lat), MIN(lon) FROM node;")
ori_x, ori_y = origin.fetchone()

#converting
dis_per_lat = 111191
dis_per_lon = 74539
node_lat[:] = [str((x_lat - ori_x)*dis_per_lat) for x_lat in node_lat]
node_lon[:] = [str((y_lon - ori_y)*dis_per_lon) for y_lon in node_lon]

#stdout
print "CREATE TABLE IF NOT EXISTS nodeCartesian (id INTEGER PRIMARY KEY, x FLOAT, y FLOAT);"
for index in range(len(node_id_list)):
    print "INSERT INTO nodeCartesian VALUES (%s,%s,%s);" % (node_id_list[index], node_lat[index], node_lon[index]) 
#close db
conn.commit()
conn.close()