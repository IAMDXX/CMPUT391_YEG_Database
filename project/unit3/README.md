# Project 3 README:

TODO: 
 * Q1:
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

 * Q2:
   - 
 :  Compiling Q2 by using the following command
   
   ```
   % cp unit3q1.db unit3q2.db
   % python3 q2.py unit3q1.db > q2_output
   % sqlite3 unit3q2.db < q2_output
   ```
   
* Q3:
   Compiling Q3 by following the instruction in __q3.md__
   
* Q4: 
   Compiling Q4 by using the following command 
   - With k=100 and lis chosen from {25, 50, 75, 100, 125}
   - Results are wrote in __q4.md__
   ```
   % python3 q4.py unit3q3_btree.db k l
   % python3 q4.py unit3q3_rtree.db k l
   ```
   
* Q5:
   Compiling Q5 by using the following command
   - Unit3q3_rtree.db is from q3
   - Coordinates x, y and parameter k finds the k areas (in areaMBR) that are closest to query point (x,y)
   ```
   % python3 q5.py unit3q3_rtree.db x y k
   ```
