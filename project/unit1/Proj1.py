# Cmput391 Project 1
# Team 20

import xml.etree.ElementTree as ET
import sqlite3
import csv
import sys
import os


conn = sqlite3.connect(":memory:")
cur = conn.cursor()

db = open("Proj1.csv","w")

def createTable():
     #cur.execute(
		#"DROP TABLE Node; DROP TABLE Way; DROP TABLE Nodetag; DROP TABLE Waytag;DROP TABLE Waypoints;"
		#)
	#generate tables
     cur.execute(
		"CREATE TABLE Node ( id INTEGER, lat FLOAT, lon FLOAT, PRIMARY KEY (id) );"
		)
	#add a CHECK closed?
     cur.execute(
		"CREATE TABLE Way ( id INTEGER PRIMARY KEY, closed BOOLEAN);"
		)
     cur.execute(
		"CREATE TABLE Waypoint ( wayid INTEGER, ordinal INTEGER, nodeid INTEGER, 						FOREIGN KEY (wayid) REFERENCES Way(id), 					FOREIGN KEY (nodeid) REFERENCES Node(id), 						CHECK ordinal>=0 AND ordinal <= COUNT(nodeid) 	 						);"
		)    
     cur.execute(
		"CREATE TABLE Nodetag ( id INTEGER, k TEXT, v TEXT, 						FOREIGN KEY (id) REFERENCES Node(id) 						);"
		)

     cur.execute(
		"CREATE TABLE Waytag ( id INTEGER, k TEXT, v TEXT, 						FOREIGN KEY (id) REFERENCES Way(id) 						);"
		)

     conn.commit()

def formatData():
     #db
     
     # Read the XML file
     tree = ET.parse('edmonton.osm')
     root = tree.getroot()
	 
     # go through all the information
     for child in root:
          print (child.tag)
          print (child.attrib)
		 
          # Insert nodes and nodetag
          if (child.tag == 'node'):
               db.write("INSERT INTO Node VALUES (" + str(child.attrib['id']) +','
	                                            + str(child.attrib['lat']) +','+ str(child.attrib['lon']) +')'  )
     
          for tag in child.iter('tag'):
               db.write("INSERT INTO Nodetag VALUES (" + str(child.attrib['id']) +','
	                                          + str(tag.attrib['k']) +','+ str(tag.attrib['v']) +")")
		 
	       # Insert ways and Waytag
	       # Need to check: 
	       # close DONE
	       # if the nodeid in the current db TODO
          if (child.tag == 'way'):
               ord = 0
               close = False	
               for ref in child.iter('ref'):
                    db.write("INSERT INTO Waypoint VALUES (" + str(child.attrib['id']) +','
	                     + str(ord) +','+ str(ref) +')'  )
                    ord += 1
  
               for tag in child.iter('tag'):
                    if 'close' in tag.attrib['v'] or 'Close' in tag.attrib['v']:
                         close = True
                         db.write("INSERT INTO Waytag VALUES (" + str(child.attrib['id']) +','
			          + str(tag.attrib['k']) +','+ str(tag.attrib['v']) +")")

               db.write("INSERT INTO Way VALUES (" + str(child.attrib['id']) +','+ str(close)  +')')

     
		                
    


def main():
    
    # Create the Database Tables
    createTable()
    
    # Load XML and insert the data
    formatData()
    
    db.close()
    ct.close()
    
if __name__ == "__main__":
	main()
