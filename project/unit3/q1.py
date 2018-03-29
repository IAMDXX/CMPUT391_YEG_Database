#cmput 391 proj #3 team20
#q1 

#Read sqlfile
print( "CREATE TABLE IF NOT EXISTS nodeCartesian (id INTEGER PRIMARY KEY, x FLOAT, y FLOAT);" )
print( "INSERT INTO nodeCartesian (id, x, y) SELECT id, ( (lon - lon_x) * 67137), ( (lat - lat_y) * 111286 ) FROM node, ( SELECT MIN(lat) AS lat_y, MIN(lon) AS lon_x FROM node ); " )

