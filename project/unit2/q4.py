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
    except:
        print("The database file doesn't exist! ")
        return

    cur = con.cursor()  
    con.create_function("nDist", 4, nodeDist)

    k = []
    v = []
    
    
    for i in argv[2:]:
        k.append(i[0:i.index('=')])
        v.append(i[i.index('=')+1:])
      
    wayids = []
    for i in range(len(k)):
        cur.execute("SELECT DISTINCT id FROM waytag WHERE k = ? AND v = ?", (k[i], v[i]))
        tmp = cur.fetchall()
        wayids += tmp
        print(wayids)

    ans = -1
    
    for wayid in wayids:
        cur.execute("SELECT DISTINCT wp.nodeid FROM way w, waypoint wp WHERE w.id = ? AND w.id=wp.wayid", (wayid[0],))
        
        nodes = cur.fetchall()
        i = 0
        dist = 0
        
        while i < len (nodes)-1: 
            cur.execute ("SELECT lat, lon FROM node WHERE node.id = ?" , (nodes[i][0],))
            (lat1, lon1) = cur.fetchall()[0]
      
            cur.execute ("SELECT lat, lon FROM node WHERE node.id = ?" , (nodes[i+1][0],))
            (lat2, lon2) = cur.fetchall()[0] 
              
            i += 1  
          
            cur.execute("select nDist(?, ?, ?, ?)", (lat1, lon1, lat2, lon2))
            
            dist += cur.fetchone()[0]
      
        if dist > ans:
            ans = dist
    
    print("The number of the paths:", len(wayids))
    print("The longest distance of the path:", ans)
    
if __name__ == "__main__":
    main(sys.argv[0:])