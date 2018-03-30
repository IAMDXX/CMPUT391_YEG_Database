# Project 3 README:

TODO: 
 * Q1
   Compiling Q1 by using the following command
   - % cp unit1.db unit3q1.db
   - % python3 q1.py unit1.db > q1_output
   - % sqlite3 unit3q1.db < q1_output 
 
 * Q2
   Compiling Q2 by using the following command  
   - % cp unit3q1.db unit3q2.db
   - % python3 q2.py unit3q1.db > q2_output
   - % sqlite3 unit3q2.db < q2_output

* Q3
   Compiling Q3 by following the instruction of q3.md
   
* Q4 
   Compiling Q4 by using the following command 
   -with k=100 and lis chosen from {25, 50, 75, 100, 125}.
   
   - % python3 q4.py unit3q3_btree.db k l
   - % python3 q4.py unit3q3_rtree.db k l
   
   Results are wrote in q4.md.
   
* Q5
   Compiling Q5 by using the following command
   - unit3q3_rtree.db is from q3
   - coordinates x, y and parameter k finds the k areas (in areaMBR) that are closest to query point (x,y).
   
   - % python3 q5.py unit3q3_rtree.db x y k
