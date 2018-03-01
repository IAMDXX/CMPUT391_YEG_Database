import os
import sys
import time
import random
import sqlite3
import math

DBFile = "edmonton.db"
db = ""

R = 6378.137 # radius of Earth in km

def nodeDist(x1,y1,x2,y2):
    
    deltaX = math.cos(x2)*math.cos(y2) - math.cos(x1)*math.cos(y1)
    deltaY = math.cos(x2)*math.sin(y2) - math.cos(x1)*math.sin(y1)
    deltaZ = math.sin(x2) - math.sin(x1)
    
    C = math.sqrt(deltaX*deltaX + deltaY*deltaY + deltaZ*deltaZ)
    
    D = R * C
    
    return D

def main(argv): 
    try:
        con = sqlite3.connect(argv[1])
        cur = con.cursor()  
        cur.execute('PRAGMA foreign_keys = ON;') 
        cur.execute ("SELECT * FROM node")        
    except:
        print("The database file doesn't exist! ")
        return

    con.create_function("nDist", 4, nodeDist)

    k = []
    v = []
    ans = 0
    num = 0
    
    for i in argv[2:]:
        k, v = i.split('=')
        
        cur.execute("WITH RECURSIVE allDist (wid, nid, dist, ord) AS (SELECT wp.wayid, wp.nodeid, 0, 0 FROM waypoint wp, mWays mw WHERE wp.wayid = mw.id AND ordinal = 0 UNION SELECT ad.wid, n2.id, ad.dist+nDist(n1.lat,n1.lon, n2.lat, n2.lon), ord+1 FROM node n1, node n2, waypoint wp, allDist ad WHERE n1.id = ad.nid AND n2.id = wp.nodeid AND wp.wayid = ad.wid AND wp.ordinal = ad.ord + 1), mWays (id) AS (SELECT DISTINCT id FROM waytag WHERE k = ? AND v = ?) SELECT max(dist) FROM allDist" ,(k, v))
        
        tmp = cur.fetchone()[0]    
        # compare the new max dist with the old one
        if tmp > ans:
            ans = tmp       
        
        cur.execute("SELECT DISTINCT id FROM waytag WHERE k = ? AND v = ?", (k, v))
        num += len(cur.fetchall())        
    
    print("The number of the paths: "+str(num))
    print("The longest distance of the path: "+str(ans)+'km')
    
if __name__ == "__main__":
    main(sys.argv[0:])