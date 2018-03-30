# Project 3 README:

## Instruction:
### Q1:
   - Created a new table __nodeCartesian(id, x, y)__
   - __id__ is the __primary key__; __x, y__ are the __Cartesian coordinates__ of nodes in __node__ table from Proj1 
   - Converting __latitude and longitude__ into Cartesian coordinates (1 unit = 1 meter) __y, x__ by using constants
   - distance_per_lat = 111,286 and distance_per_log = 67,137 
   - URL:https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=967003
   - In table nodeCartesian, x = (maxlon - minlon) * distance_per_log; y = (maxlat - minlat) * distance_per_lat
   - unit1.db is a legal database conforming to the specs of Unit 1
   -  __your program should not modify the database at all__
   - instead, it should print the SQL commands to modify the database to __STDOUT__ (q1_output)
  
  : Compiling Q1 by using the following command
   
   ```
   % cp unit1.db unit3q1.db
   % python3 q1.py unit1.db > q1_output
   % sqlite3 unit3q1.db < q1_output
   ```

### Q2:
   - Create a table areaMBR(id, minX, maxX, minY, maxY); __id__ is the __primary key__
   - Store the id and the Cartesian coordinates of the __minimum bounding__ rectangle of every __closed__ way 
   
 :  Compiling Q2 by using the following command
   
   ```
   % cp unit3q1.db unit3q2.db
   % python3 q2.py unit3q1.db > q2_output
   % sqlite3 unit3q2.db < q2_output
   ```
   
### Q3:
   - Create two SQLite databases: __unit3q3_btree.db__ and __unit3q3_rtree.db__
   - __unit3q3_btree.db__: separate single column __B+tree__ indexes on each of the coordinates of the areaMBR 
   - __unit3q3_rtree.db__: a 2D __R-tree__ index populated with the areas of the areaMBR
   - __Note__ : You have to run Q1 and Q2 first
   
:  Compiling Q3 by following the instruction in __q3.md__
   
### Q4: 
   - Comparing the execution times of similar queries on __unit3q3_btree.db__ and __unit3q3_rtree.db__
   - Computes the average time out of k=100 runs and l is chosen from {25, 50, 75, 100, 125}
   - To find the number of areas from areaMBR that are contained in a randomly generated bounding rectangle
   - The rectangle has width __l*rand(1,10)__ and height __l*rand(1,10)__; 
   - where rand(x,y) stands for a floating point number between x and y, randomly chosen using a uniform distribution
   - The rectangle __overlaps__ with at least one MBR in the areaMBR table.
   - The point corresponding to the __bottom-left__ corner of the rectangle is randomly chosen following a uniform distribution
   - __Note__ : Results are wrote in __q4.md__
   
:  Compiling Q4 by using the following command 

   ```
   % python3 q4.py unit3q3_btree.db k l
   % python3 q4.py unit3q3_rtree.db k l
   ```
   
### Q5:
   - Implementing the algorithm for answering nearest neighbor queries described in the __NN.pdf__ paper:
     - N. Roussopoulos, S. Kelley, and F. Vincent. Nearest neighbor queries. InProceedings of the 1995 ACM SIGMOD International Conference on Management of Data, San Jose, California, May 22-25, 1995., 71-79. ACM Press, 1995.doi:10.1145/223784.223794. 
   - Unit3q3_rtree.db is from q3
   - Coordinates x, y and parameter k finds the k areas (in areaMBR) that are closest to query point (x,y)
   - STDOUT the ids of result areas and their distance to the query point, sorted by increasing distance
   - The distance between the query point Q and an area A should be the __Euclidean distance__ between Q and the geodesic centre of A
   - __Euclidean distance__ between (a, b) and (x, y): sqrt(a−x)2+(b−y)2)
   - __geodesic centre__ of area with coordinate (minX, minY, maxX, maxY): ((maxX-minX)/2, (maxY-minY)/2) 

:  Compiling Q5 by using the following command
   
   ```
   % python3 q5.py unit3q3_rtree.db x y k
   ```
