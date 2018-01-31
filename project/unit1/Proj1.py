# Cmput391 Project 1
# Team 20

import xml.etree.ElementTree as ET
import sqlite3
import csv
import sys
import os


conn = sqlite3.connect(":memory:")
cur = conn.cursor()

nf = open("nf.csv","w")
wf = open("wf.csv","w")
wp = open("wp.csv","w")
nt = open("nt.csv","w")
wt = open("wt.csv","w")

nodes = []

def createTable():
    #drop previous exist tables
    cur.execute( "DROP TABLE IF EXISTS Node ;")
    cur.execute( "DROP TABLE IF EXISTS Way ;")
    cur.execute( "DROP TABLE IF EXISTS Waypoint ;")
    cur.execute( "DROP TABLE IF EXISTS Nodetag ;")
    cur.execute( "DROP TABLE IF EXISTS Waytag ;")

    #generate tables
    cur.execute(
         "CREATE TABLE Node ( id INTEGER, lat FLOAT, lon FLOAT, PRIMARY KEY (id) );"
    )
    cur.execute(
        "CREATE TABLE Way ( id INTEGER PRIMARY KEY, closed BOOLEAN );"
    )
    cur.execute(
         "CREATE TABLE Waypoint ( wayid INTEGER, ordinal INTEGER, nodeid INTEGER, FOREIGN KEY (wayid) REFERENCES Way(id), FOREIGN KEY (nodeid) REFERENCES Node(id), CHECK (ordinal>=0 AND ordinal <= rowid ) );"
    )    
    cur.execute(
         "CREATE TABLE Nodetag ( id INTEGER, k TEXT, v TEXT, FOREIGN KEY (id) REFERENCES Node(id) );"
    )

    cur.execute(
         "CREATE TABLE Waytag ( id INTEGER, k TEXT, v TEXT, FOREIGN KEY (id) REFERENCES Way(id) );"
    )

    conn.commit()

def formatData():
     #db
     
     # Read the XML file
    tree = ET.parse('edmonton.osm')
    root = tree.getroot()
	 
    # go through all the information
    for node in root.iter('node'): 
	# Insert nodes and nodetag
        nf.write(str(node.attrib['id']) +','+ str(node.attrib['lat']) +','+ str(node.attrib['lon']) )
        if (node.attrib['id'] not in nodes):
            nodes.append(node.attrib['id'])
   
        for tag in node.iter('tag'):
            nt.write(str(node.attrib['id']) +','+ str(node.attrib['k']) +','+ str(node.attrib['v']) )
		
    # Insert ways and Waytag
    # Need to check: 
    # close DONE
    # if the nodeid in the current db TODO
    for way in root.iter('way'):
        close = False
        discard = False
        way_pts = []
        for ref in way.iter('nd'):
            if (ref.attrib['ref'] in nodes):
                way_pts.append(ref.attrib['ref'])
            else:
                discard = True
                break
        if discard == True:
            continue
	    
        ord = 0
        for way_p in way_pts:
            wp.write(str(way.attrib['id']) +','+ str(ord) +','+ str(way_p) )
            ord += 1
	    
        if way_pts[0] == way_pts[-1]:
            close = True

        for tag in way.iter('tag'):
            if 'close' in tag.attrib['v'] or 'Close' in tag.attrib['v']:
                close = True
            wt.write(str(way.attrib['id']) +','+ str(tag.attrib['k']) +','+ str(tag.attrib['v']) )

        wf.write(str(way.attrib['id']) +','+ str(close))

    nf.close()
    wf.close()
    nt.close()
    wt.close()
    wp.close()
			       
    


def main():
    
    # Create the Database Tables
    createTable()
    
    # Load XML and insert the data
    formatData()
    
    
if __name__ == "__main__":    
    main()