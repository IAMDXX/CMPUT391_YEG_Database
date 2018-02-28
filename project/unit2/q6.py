#cmput 391 proj #2 team20
# q6
import sys
import csv
import sqlite3

db_file = "edmonton.db" #sys.argv[1]
tsv_file = "way.tsv" #sys.argv[2]

#connet to database
conn = sqlite3.connect(db_file)
cur = conn.cursor()
#turn on foreign key verification
cur.execute('PRAGMA foreign_keys = ON;') 

#read from tsv file
with open(tsv_file) as tsvfile:
    tsvreader = list(csv.reader(tsvfile, delimiter='\t'))
    
    #slicing tsvreader into two lists: WAYS contains all ways with id and tag; NODES contains all nodes of corresponding way
    WAYS = tsvreader[0:len(tsvreader):3]
    NODES = tsvreader[1:len(tsvreader):3]
    for i in range(len(WAYS)):
        curr_way = WAYS[i]
        curr_waypoints = NODES[i]

        wayid = int(curr_way[0])
        tag = curr_way[1:]
       
        # check if the way is a closed path
        first = int(curr_waypoints[0])
        last = int(curr_waypoints[-1])
        if first == last:
            closed = 1
        else:
            closed = 0
       
        #inserting way
        cur.execute("INSERT INTO Way(id, closed) VALUES (?,?);", (wayid,closed))
        conn.commit() 
        
        #inserting nodes in the path 
        for i in range (len(curr_waypoints)):
            cur.execute("INSERT INTO Waypoint(wayid, ordinal, nodeid) VALUES (?,?,?);", (wayid, i, int(curr_waypoints[i])))
            conn.commit()
            
#commit and close database
    #conn.commit() 
    conn.close()   