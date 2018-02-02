# Project 1 README:

Task:

To write and document code to extract all nodes, paths and areas (closed paths) within the City of Edmonton and store them in a SQLite database, together with descriptive tags associated with them.



Instuction:
Run: proj1.py with data file: % python proj1.py

  1. We choose to use CSV for this assignment.
  2. Use iterparse to get the data from osm file which is much faster than parse.
  3. According to the tag, we act differently:
  
      Node: save into csv file and go through all the related tags and save them
  
      Way: save all the way points and do the check at the same time:
      
          a. if the nodeid is not in the db, discard the whole way
          
          b. if the number of nodes in the way is less than 2, discard the way
          
      save all the tags and save them into csv if way is not discarded
      
  4. Transfer all the data in CSV files to the db
  5. Add triggers for checking any INSERT/DELETE/UPDATE on Waypoint that will changes closed constrains;
      And the trigger for checking ordinal number in Waypoint
  
  
  
At present we just done for small data and it runs perfectly but for the orignal data we have some issue that can't be solved.

Issue: data about way can't be written into the CSV file.

