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

