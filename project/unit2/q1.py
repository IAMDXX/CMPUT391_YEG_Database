import os
import sys
import time
import random
import sqlite3
import math

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
    
    nid1 = int(argv[2])
    nid2 = int(argv[3])
    #print(nid1, nid2)
    
    con.create_function("nDist", 4, nodeDist)
    
    cur.execute("select nDist(n1.lat,n1.lon, n2.lat, n2.lon) FROM node n1, node n2 WHERE n1.id = ? AND n2.id = ?", 
                        (nid1, nid2))
    print ("The distance between this two nodes is: "+str(cur.fetchone()[0])+'km')


if __name__ == "__main__":
    main(sys.argv[0:])