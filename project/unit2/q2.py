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
    k = []
    v = []
    
    ans = -1
    
    for i in argv:
      k.append(i[0:i.index('=')])
      v.append(i[i.index('=')+1:])
      
    cur.executemany("SELECT DISTINCT id FROM nodetag WHERE k = %s AND v = %s", (k, v))
    
    nodes = cur.fetchall()
    
    for i in range(len(nodes)-1):
      cur.execute ("SELECT lat, lon FROM node WHERE node.id = '%d'" , nodes[i])
      lat1, lon1 = cur.fetchall()
      for j in range(i+1,len(nodes)):
        cur.execute ("SELECT lat, lon FROM node WHERE node.id = '%d'" , nodes[j])
        lat2, lon2 = cur.fetchall() 
        
        
    
        cur.execute("select nDist(?, ?, ?, ?)", (lat1, lon1, lat2, lon2))
        
        if cur.fetchone()[0] > ans:
          ans = cur.fetchone()[0]

    print("The number of the nodes:", len(nodes))
    print("The longest distance between the nodes:", ans)

if __name__ == "__main__":
    main(sys.argv[0:])