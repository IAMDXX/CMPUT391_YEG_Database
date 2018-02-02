# Cmput391 Project 1
# Team 20
import csv
import xml.etree.ElementTree as ET
import sqlite3

#sqlite_add = '/Users/DXX/Desktop/UACLASS/CMPUT391/proj1/proj1.db'
#conn = sqlite3.connect(sqlite_add)


parser = ET.iterparse('test.osm')
conn = sqlite3.connect("./proj1.db")
cur = conn.cursor()  
nodes = dict()



def formatData():
    #db

    # Read the XML file
    csvfile1 = open('nf.csv','wb')
    csvfile2 = open('nt.csv','wb')
    csvfile3 = open('wp.csv','wb')
    csvfile4 = open('wt.csv','wb')
    csvfile5 = open('wf.csv','wb')
    #root = tree.getroot()

    # go through all the information
    #with open('nf.csv', 'wb') as csvfile1, open('nt.csv', 'wb') as csvfile2, open('wp.csv', 'wb') as csvfile3, open('wt.csv', 'wb') as csvfile4, open('wf.csv', 'wb') as csvfile5:
        #fieldnames = ['id', 'lat', 'lon']
    writer1 = csv.writer(csvfile1)
    #fieldnames = ['id', 'k', 'v']
    writer2 = csv.writer(csvfile2)   
    
    f3 = ['id','ordi','nodeid']
    writer3 = csv.DictWriter(csvfile3,fieldnames = f3)
    writer3.writeheader()
    
    f4 = ['id','k','v']
    writer4 = csv.DictWriter(csvfile4,fieldnames = f4)
    writer4.writeheader()
    
    f5 = ['id','closed']
    writer5 = csv.DictWriter(csvfile5,fieldnames = f5)
    writer5.writeheader()        
           
    for event, element in parser:
        # Insert nodes and nodetag
        if element.tag == 'node':
            writer1.writerow( [str(element.attrib['id']), str(element.attrib['lat']) ,str(element.attrib['lon'])] )
            nodes[element.attrib['id']] = 0
            for tag in element.iter('tag'):
                writer2.writerow( [str(element.attrib['id']), tag.attrib['k'].encode('utf-8'), tag.attrib['v'].encode('utf-8')] )                

            element.clear()            
            
        # Insert ways and Waytag
        # Need to check: 
        # close DONE
        # if the nodeid in the current db TODO    
#with open('wp.csv', 'wb') as csvfile3, open('wt.csv', 'wb') as csvfile4, open('wf.csv', 'wb') as csvfile5:
     
        if element.tag == 'way':
            close = False
            discard = False
            way_pts = []
            ordi = 0
            for ref in element.iter('nd'):
                
                if (ref.attrib['ref'] in nodes.keys()):
                    way_pts.append(ref.attrib['ref'])
                else:
                    discard = True
                    break
            if discard == True or len(way_pts) <=1:
                continue
    
            if way_pts[0] == way_pts[-1]:
                close = True
                
            k = dict()
            v = dict()
            for tag in element.iter('tag'):
                k[ordi] = (tag.attrib['k'])
                v[ordi] = (tag.attrib['v'])
                ordi += 1
            
            writer5.writerow({'id': str(element.attrib['id']), 'closed': str(close)})
            
            for i in range(len(way_pts)):
               # row = "{'id': " + str(element.attrib['id'])+", 'ordi': "+ str(i) + ", nodeid': "+ str(way_p[i])+"}"
                writer3.writerow( {'id': str(element.attrib['id']), 'ordi': str(i), 'nodeid': str(way_pts[i])} )
            
            for i in range(len(k)):
                writer4.writerow({'id': str(element.attrib['id']), 'k': k[i].encode('utf-8'), 'v': v[i].encode('utf-8')} )
                
            element.clear()
    csvfile1.close()
    csvfile2.close()
    csvfile3.close()
    csvfile4.close()
    csvfile5.close()
            
def impCSV():
    with open('nf.csv','rb') as fin: 
        dr = csv.reader(fin)
        to_db = [(i[0], i[1], i[2]) for i in dr]
    cur.executemany("INSERT INTO Node (id, lat, lon) VALUES (?, ?, ?);", to_db)
    
    with open('wf.csv','rb') as fin: 
        dr = csv.DictReader(fin)
        for i in dr:
            cur.execute("INSERT INTO Way (id, closed) VALUES (?, ?);",(i['id'],i['closed']) )
    conn.commit()
    
    with open('nt.csv','rb') as fin: 
        dr = csv.reader(fin)
        to_db = [(i[0], str(i[1].decode('utf-8')), str(i[2]).decode('utf-8')) for i in dr]
    cur.executemany("INSERT INTO Nodetag (id, k, v) VALUES (?, ?, ?);", to_db)
    
    with open('wt.csv','rb') as fin: 
        dr = csv.DictReader(fin)
        for i in dr:
            cur.execute("INSERT INTO Waytag (id, k, v) VALUES (?, ?, ?);", (i['id'],i['k'].decode('utf-8'),i['v'].decode('utf-8')))
    
    with open('wp.csv','rb') as fin: 
        dr = csv.DictReader(fin)
        for i in dr:
            cur.execute("INSERT INTO Waypoint (wayid, ordinal, nodeid) VALUES (?, ?, ?);", (i['id'], i['ordi'], i['nodeid']))    
    
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
         "CREATE TABLE Waypoint ( wayid INTEGER, ordiinal INTEGER, nodeid INTEGER, FOREIGN KEY (wayid) REFERENCES Way(id), FOREIGN KEY (nodeid) REFERENCES Node(id), CHECK (ordiinal>=0 AND ordiinal < rowid ) );"
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
