# Project 2 README:

## Instrucion:

ASSUMPTION :
  * all the inputs for 1-4 are valid, ie exist in the database
  * for 'key=value', there is no space in this whole arguement

Q1: $ python q1.py edmonton.db nodeid1 nodeid2

Q2: $ python q2.py edmonton.db key1=value1 key2=value2...

Q3: $ python q3.py edmonton.db wayid

Q4: $ python q4.py edmonton.db key1=value1 key2=value2...

Q5: $ python q5.py edmonton.db sample_node_file.tsv

Q6: $ python q6.py edmonton.db sample_way_file.tsv


## Question 1:

Use Haversine formula to calculate the distance between two points on the earth.
Reason: We can assume the earth is nearly spherical, so great-circle distance formulas, ie Haversine formula, can give the distance between points on the surface of the Earth within and error in about 0.5%.

## Question 2:

Grab the nodes matching each tag values and then calculate the distances of two points in this table. And finally use MAX() to find the max value in this table. Then store the max value for each k,v and compare them to get the final result.

## Question 3:

Recurssion with (wid, nodeid, dist, ord):
* dist is accumulated, ie the distance from the first point to the current point
* ord is the ordinal in the waypoint which is used to pair two neighbor points

## Question 4:

Grab the ways matching each tag values and then calculate the distance of ways. Then use MAX() to get the largest one and store them. When it comes to another new (k,v) pair, compute again and compare to get the final result.

## Question 5:

Open the database which is passing from the command.
Turn on foreign key verification by executing 'PRAGMA foreign_keys = ON;' in database.
Reading the given tsv file row by row and seprate by tabs into a list.
Inserting the first 3 values as (id, lat, lon) into node table and the rest columns as strings of the form key=values.
Inserting node id and coressponding key and values into nodetag table.
commit all changes and closed the database.

## Question 5:

Open the database which is passing from the command.
Turn on foreign key verification by executing 'PRAGMA foreign_keys = ON;' in database.
Reading the given tsv file and seprate by tabs into a list.
Then slice the tsvreader list into two lists. The first list contains the every first non-blank row in the tsv file which contains wayids and tags for way; The second list contains every second non-blank row in tsv file, which contains nodes in the corresponding ways.

We first read the first value from the first list as wayid, and checking closed if the first node in that way is equal to the last nodeid. Inserting wayid and closed=1 if the way is closed into way table, otherwise inserting (wayid,0) into way table. And inseritng the rest columns in the first list as strings of the form key=values.
Inserting nodeids in the second columnnd and corresponding wayid with order number into waypoint tables.
Inserting coressponding key and values into waytag table.
commit all changes and closed the database.
