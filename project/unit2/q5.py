#cmput 391 proj #2 team20
#q5 
import sys
import csv
import sqlite3

db_file = sys.argv[1]
tsv_file = sys.argv[2]

#connet to database
conn = sqlite3.connect(db_file)
cur = conn.cursor()
#turn on foreign key verification
cur.execute('PRAGMA foreign_keys = ON;') 

#read from tsv file
with open(tsv_file) as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter='\t')
    for line in tsvreader:
        nodeid = int(line[0])
        lat= float(line[1])
        lon = float(line[2])
        cur.execute("INSERT INTO Node (id, lat, lon) VALUES (?,?,?);", (nodeid, lat, lon))
        conn.commit()
        
        #inserting tags for nodes
        tags = line[3:]
        for i in tags:
            key,value = i.split('=')
            cur.execute("INSERT INTO Nodetag (id, k, v) VALUES (?,?,?);", (nodeid, key, value))
            conn.commit() 
# close database   
conn.close()   
 