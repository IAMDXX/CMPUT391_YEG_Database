import os
import sys
import time
import random
import sqlite3
import math

DBFile = "edmonton.db"
db = ""

R = 6378.137 # radius of Earth in km

def nodeDist(la1,lo1,la2,lo2):
    
    x1 = math.radians(la1)
    y1 = math.radians(lo1)
    x2 = math.radians(la2)
    y2 = math.radians(lo2)
    
    dx = x2-x1
    dy = y2-y1
    
    a = math.sin(dx / 2)**2 + math.cos(x1) * math.cos(x2) * math.sin(dy/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))    
    
    d = R * c
    
    return d

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
    nodes = {}
    
    # get the number of the nodes
    for i in argv[2:]:
        k, v = i.split('=')
        cur.execute("SELECT DISTINCT id FROM nodetag WHERE k = ? AND v = ?", (k, v))
        tmp = cur.fetchall()
        for j in tmp:
            if j[0] not in nodes.keys():
                nodes[j[0]] = 0
        
    for i in argv[2:]:
        k, v = i.split('=')
        
        # get the max dist
        cur.execute("With mNodes (id, lat, lon) AS (SELECT DISTINCT n.id, n.lat, n.lon FROM node n, nodetag nt WHERE nt.k = ? AND nt.v = ? AND nt.id = n.id ) SELECT max(nDist(n1.lat,n1.lon, n2.lat, n2.lon)) FROM mNodes n1, mNodes n2", (k,v))
        tmp = cur.fetchone()[0]    
        #print(tmp)
        # compare the new max dist with the old one
        if tmp > ans:
            ans = tmp 

    

    print("The number of the nodes: "+str(len(nodes)))
    print("The longest distance between the nodes: "+str(ans)+'km')

if __name__ == "__main__":
    main(sys.argv[0:])