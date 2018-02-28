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
    cur.execute('PRAGMA foreign_keys = ON;') 
    
    nid1 = int(argv[2])
    nid2 = int(argv[3])
    #print(nid1, nid2)
    
    # get the lat and long of 2 nodes
    cur.execute ("SELECT lat, lon FROM node WHERE node.id = '%d'" % nid1)
    (lat1, lon1) = cur.fetchall()[0]
    
    cur.execute ("SELECT lat, lon FROM node WHERE node.id = '%d'" % nid2)
    (lat2, lon2) = cur.fetchall()[0]    
    
    con.create_function("nDist", 4, nodeDist)
    
    cur.execute("select nDist(?, ?, ?, ?)", (lat1, lon1, lat2, lon2))
    print ("The distance between this two nodes is: "+str(cur.fetchone()[0])+'km')


if __name__ == "__main__":
    main(sys.argv[0:])