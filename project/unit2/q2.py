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
        
        # get the max dist
        cur.execute("With mNodes (id, lat, lon) AS (SELECT DISTINCT n.id, n.lat, n.lon FROM node n, nodetag nt WHERE nt.k = ? AND nt.v = ? AND nt.id = n.id ) SELECT max(nDist(n1.lat,n1.lon, n2.lat, n2.lon)) FROM mNodes n1, mNodes n2", (k,v))
        tmp = cur.fetchone()[0]    
        #print(tmp)
        # compare the new max dist with the old one
        if tmp > ans:
            ans = tmp
        # get the number of the nodes 
        cur.execute("SELECT DISTINCT id FROM nodetag WHERE k = ? AND v = ?", (k, v))
        num += len(cur.fetchall())
    

    print("The number of the nodes: "+str(num))
    print("The longest distance between the nodes: "+str(ans)+'km')

if __name__ == "__main__":
    main(sys.argv[0:])