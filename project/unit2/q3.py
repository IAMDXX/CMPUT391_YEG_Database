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
    
    C = sqrt(deltaX^2 + deltaY^2 + deltaZ^2)
    
    D = R * C
    
    return D

def main(argv): 
    try:
        con = sqlite3.connect(argv[0])
    except:
        print("The database file doesn't exist! ")
        return
    global con
    cur = con.cursor()  
    con.create_function("nDist", 4, nodeDist)

    ans = -1
    
    wayid = int(argv[1])
     
    cur.execute("SELECT DISTINCT wp.nodeid FROM way w, waypoint wp WHERE w.id = %d AND w.id=wp.wayid", wayid)
    
    nodes = cur.fetchall()
    i = 0
    
    while i < len (nodes): 
      cur.execute ("SELECT lat, lon FROM node WHERE node.id = '%d'" , nodes[i])
      lat1, lon1 = cur.fetchall()

      cur.execute ("SELECT lat, lon FROM node WHERE node.id = '%d'" , nodes[i+1])
      lat2, lon2 = cur.fetchall() 
        
      i += 1  
    
      cur.execute("select nDist(?, ?, ?, ?)", (lat1, lon1, lat2, lon2))
      
      ans += cur.fetchone()[0]

    print("The length of the way is :", ans)
    
if __name__ == "__main__":
    main(sys.argv[0:])