#cmput 391 proj #3 team20
#q1 

#Read sqlfile
print( "CREATE TABLE IF NOT EXISTS nodeCartesian (id INTEGER PRIMARY KEY, x FLOAT, y FLOAT);" )
print( "INSERT INTO nodeCartesian (id, x, y) SELECT id, ( (lat - lat_x) * 111286), ( (lon - lon_y) * 67137 ) FROM node, ( SELECT MIN(lat) AS lat_x, MIN(lon) AS lon_y FROM node ); " )

