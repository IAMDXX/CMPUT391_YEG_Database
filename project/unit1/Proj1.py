# Cmput391 Project 1
# Team 20
# Cmput391 Project 1
# Team 20

import csv
import xml.etree.ElementTree as ET
import sqlite3

#sqlite_add = '/Users/DXX/Desktop/UACLASS/CMPUT391/proj1/proj1.db'
#conn = sqlite3.connect(sqlite_add)


parser = ET.iterparse('edmonton.osm')
conn = sqlite3.connect(":memory:")
cur = conn.cursor()  
nodes = dict()

def formatData():
    #db

    # Read the XML file

    #root = tree.getroot()

    # go through all the information
    with open('nf.csv', 'wb') as csvfile1, open('nt.csv', 'wb') as csvfile2, open('wp.csv', 'wb') as csvfile3, open('wt.csv', 'wb') as csvfile4, open('wf.csv', 'wb') as csvfile5:
        #fieldnames = ['id', 'lat', 'lon']
        writer1 = csv.writer(csvfile1)
        #fieldnames = ['id', 'k', 'v']
        writer2 = csv.writer(csvfile2)   
        
        f3 = ['id','ord','nodeid']
        writer3 = csv.DictWriter(csvfile3,fieldnames = f3)
        writer3.writeheader()
        
        f4 = ['id','k','v']
        writer4 = csv.DictWriter(csvfile4,fieldnames = f4)
        writer4.writeheader()
        
        f5 = ['id','close']
        writer5 = csv.DictWriter(csvfile5,fieldnames = f5)
        writer5.writeheader()        
               
        for event, element in parser:
            # Insert nodes and nodetag
            if element.tag == 'node':
                writer1.writerow( [str(element.attrib['id']), str(element.attrib['lat']) ,str(element.attrib['lon'])] )
                nodes[element.attrib['id']] = 0
            #for tag in element.iter('tag'):
                #writer2.writerow( [str(element.attrib['id']), tag.attrib['k'].encode('utf-8'), tag.attrib['v'].encode('utf-8')] )                

                element.clear()            
                
            # Insert ways and Waytag
            # Need to check: 
            # close DONE
            # if the nodeid in the current db TODO    
    #with open('wp.csv', 'wb') as csvfile3, open('wt.csv', 'wb') as csvfile4, open('wf.csv', 'wb') as csvfile5:
         
            if element.tag == 'way':
                start = 0
                end = 0
                close = False
                discard = False
                way_pts = []
                for ref in element.iter('nd'):
                    
                    if (ref.attrib['ref'] in nodes.keys()):
                        way_pts.append(ref.attrib['ref'])
                    else:
                        discard = True
                        break
                #if discard == True:
                    #continue
        
                ord = 0
    
                for way_p in way_pts:
                    if ord == 0:
                        start = way_p
                    if ord == len(way_pts)-1:
                        end = way_p
                    writer3.writerow( {'id': str(element.attrib['id']), 'ord': str(ord), 'nodeid': str(way_p)} )
                    ord += 1
        
                if start == end:
                    close = True
                    
                for tag in element.iter('tag'):
                    if 'close' in tag.attrib['v'] or 'Close' in tag.attrib['v']:
                        close = True
                    writer4.writerow({'id': str(element.attrib['id']), 'k': tag.attrib['k'].encode('utf-8'), 'v':tag.attrib['v'].encode('utf-8')} )
                    
                writer5.writerow({'id': str(element.attrib['id']), 'close': str(close)})
                
                element.clear()
    
            
def impCSV():
    print("DONE")
    with open('nf.csv','rb') as fin: 
        dr = csv.reader(fin)
        to_db = [(i[0], i[1], i[2]) for i in dr]
    cur.executemany("INSERT INTO Node (id, lat, lon) VALUES (?, ?, ?);", to_db)
    
    with open('wf.csv','rb') as fin: 
        dr = csv.reader(fin)
        to_db = [(i[0], i[1]) for i in dr]
    cur.executemany("INSERT INTO Way (id, closed) VALUES (?, ?);", to_db)
    conn.commit()
    
    with open('nt.csv','rb') as fin: 
        dr = csv.reader(fin)
        to_db = [(i[0], str(i[1]), str(i[2])) for i in dr]
    cur.executemany("INSERT INTO Nodetag (id, k, v) VALUES (?, ?, ?);", to_db)
    
    with open('wt.csv','rb') as fin: 
        dr = csv.DictReader(fin)
        to_db = [(i[0], str(i[1]), str(i[2])) for i in dr]
    cur.executemany("INSERT INTO Waytag (id, k, v) VALUES (?, ?, ?);", to_db)
    
    with open('wp.csv','rb') as fin: 
        dr = csv.reader(fin)
        to_db = [(i[0], i[1], str(i[2])) for i in dr]
    cur.executemany("INSERT INTO Waypoint (wayid, ordinal, nodeid) VALUES (?, ?, ?);", to_db)    
    
    conn.commit()
    conn.close()   

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
         "CREATE TABLE Waypoint ( wayid INTEGER, ordinal INTEGER, nodeid INTEGER, FOREIGN KEY (wayid) REFERENCES Way(id), FOREIGN KEY (nodeid) REFERENCES Node(id), CHECK (ordinal>=0 AND ordinal < rowid ) );"
    )    
    cur.execute(
         "CREATE TABLE Nodetag ( id INTEGER, k TEXT, v TEXT, FOREIGN KEY (id) REFERENCES Node(id) );"
    )

    cur.execute(
         "CREATE TABLE Waytag ( id INTEGER, k TEXT, v TEXT, FOREIGN KEY (id) REFERENCES Way(id) );"
    )

    conn.commit()



def main():

    # Create the Database Tables
    createTable()

    # Load XML and insert the data
    formatData()
    
    # Load CSV into database
    impCSV()    


if __name__ == "__main__":    
    main()
