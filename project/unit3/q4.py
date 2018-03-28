import os
import sys
import time
import random as rand
import sqlite3
import math


def main(argv):
     con = sqlite3.connect(argv[1])
     cur = con.cursor()       
     
     l = int(argv[2])
     k = int(argv[3])
     
     cur.execute ("select max(x),max(y) from nodeCartesian")
     max_x,max_y= cur.fetchone()
     
     run_time = 0
     
     for execute in range(k):
          h = l * rand.uniform(1, 10)
          w = l * rand.uniform(1, 10)        
          x1 = rand.uniform(0,max_x)
          y1 = rand.uniform(0,max_y)
          x2 = x1 + w
          y2 = y1 + h
          
          # Check if there's a overlap
          stmt = "SELECT COUNT(*) FROM areaMBR a WHERE (? BETWEEN a.minX and a.maxX AND ? BETWEEN a.minY AND maxY) OR (? BETWEEN a.minX and a.maxX AND ? BETWEEN a.minY AND maxY) \
          OR (? BETWEEN a.minX and a.maxX AND ? BETWEEN a.minY AND maxY) OR (? BETWEEN a.minX and a.maxX AND ? BETWEEN a.minY AND maxY)"
          
          cur.execute(stmt, (x1,y1, x1,y2, x2,y1, x2,y2))
          ol = cur.fetchone()
          
          if(ol[0] < 1):
               execute -= 1
               continue
          
          # Begin to record time
          stmt = "SELECT COUNT(*) FROM areaMBR a WHERE a.minX BETWEEN ? and ? AND a.maxX BETWEEN ? and ? AND a.minY BETWEEN ? and ? AND a.maxY BETWEEN ? and ?"
          
          start_time = time.time()
          cur.execute(stmt, (x1,x2, x1,x2, y1,y2, y1,y2))
          end_time = time.time()
          
          run_time += (end_time-start_time)
          
     print(str(k) + '\t' + str(l) + '\t' + str(run_time/k))
     
if __name__ == "__main__":
     main(sys.argv[0:])
