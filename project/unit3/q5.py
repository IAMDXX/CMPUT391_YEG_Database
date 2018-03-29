import os
import sys
import time
import random as rand
import sqlite3
import math

class NODES:
     def _init_(self):
          self.nid = 0
          self.pruned = False
          self.min_d = float("inf")
          self.minmax_d = float("inf")
          self.pts = [0.0, 0.0, 0.0, 0.0]
          self.td = 0
          
cord = [0, 0] 
k = 0
NN_nid = []
NN_d = []
con = ""
cur = ""

# K-Nearest Neighbor Search
def KNN(nodeno):
     
     stmt = "SELECT count(*) FROM areaMBR_parent ap WHERE ap.parentnode = ?"
     cur.execute(stmt, (node,))
     num_node = cur.fetchone()[0]
     
     # if leaf
     if (num_node == 0):
          calLeafDist(nodeno)
          return 
     
     # Non-leaf level - order, prune, travel
     
     # 1. generate branch list
     nlist = []
     tmplist = []
     stmt = "SELECT ap.nodeno FROM areaMBR_parent ap WHERE ap.parentnode = ?"
     cur.execute (stmt, (nodeno,))
     tmplist = cur.fetchall()
     
     for i in tmplist:
          nlist.append(i[0])
     
     # 2. sort the list we got
     brlist = [NODES() for i in range(num_node)]
     
     for i in range(num_node):
          stmt = "SELECT rtreenode(2, data) FROM areaMBR_node WHERE nodeno = ?; "
          cur.execute (stmt, (nlist[i], ))       
          tmpdata = cur.fetchone()
          brlist[i].nid = tmpdata[0]
          brlist[i].pts = tmpdata[1:]
     
     # 2.1 calculate the distance
     for i in range(num_node):
          a = 0
          b1 = 0
          b2 = 0
          c = 0
          # 2.1.1 calculate minimum for x (ie n=1)
          s = brlist[i].pts[0]
          t = brlist[i].pts[1]
          if (cord[0] < s):
               r = s
          elif (cord[0] > p):
               r = p
          else:
               r  = cord[0]
          a += (cord[0]-r)*(cord[0]-r)
          # 2.1.2 calculate minmax for x (ie n=1)
          if (cord[0] <= (s+t)/2):
               rm = s
          else:
               rm = t
          b1 += (cord[0]-rm)*(cord[0]-rm)
          
          if (cord[0] >= (s+t)/2):
               rM = s
          else:
               rM = t
          c += (cord[0]-rM)*(cord[0]-rM)   
          
          # 2.1.3 calculate minimum for y (ie n=2)
          s = brlist[i].pts[2]
          t = brlist[i].pts[3]
          if (cord[1] < s):
               r = s
          elif (cord[1] > p):
               r = p
          else:
               r  = cord[1]
          a += (cord[1]-r)*(cord[1]-r)  
          
          # 2.1.4 calculate minmax for y (ie n=2)
          if (cord[1] <= (s+t)/2):
               rm = s
          else:
               rm = t
          b2 += (cord[1]-rm)*(cord[1]-rm)
          
          if (cord[1] >= (s+t)/2):
               rM = s
          else:
               rM = t
          c += (cord[1]-rM)*(cord[1]-rM)            
          
          brlist[i].min_d = a
          brlist[i].td = a 
          if ((b1 + c) < (b2 + c)):
               brlist[i].minmax_d = b1 + c
          else:
               brlist[i].minmax_d = b2 + c
          
     # 2.2 perform downward pruning
     for i in range(num_node):
          done = False
          for j in range(num_node):
               if (i != j and brlist[i].min_d > brlist[j].minmax_d):
                    brlist[i].pruned = True
                    done = True
               if done:
                    break
               
     # 2.3 sort 
     min_id = 0
     for i in range(num_node):
          done = False
          for j in range(num_node):     
               if brlist[j].td < brlist[min_id].td:
                    min_id = j
          if (brlist[i].pruned):
               nlist[j] = -1
          else:
               nlist[j] = brlist[min_id].nid
          brlist[i].td = float('inf') # the point is visited
          
     # 3 travel through the child nodes
     for i in range(num_node):
          if (nlist[i] != -1):
               KNN(nlist[i])
    
    
          
# Calcualte the distance to actual object
def calLeafDist (nodeno):
     
     stmt = "SELECT a.id,a.minX,a.maxX,a.minY,a.maxY FROM areaMBR_rowid ar, areaMBR a WHERE a.id = ar.rowid and ar.nodeno = ? group by a.id"
     cur.execute(stmt, (nodeno,))
     tstr = cur.fetchone()
     nid = tstr[0]
     x = (tstr[1]+tstr[2])/2
     y = (tstr[3]+tstr[4])/2
     
     tmpd = math.sqrt((cord[0]-x)*(cord[0]-x) + (cord[1]-y)*(cord[1]-y))
     tmpid = 0
     
     # Replace the larger values with the smaller ones
     for i in range(k):
          if (tmpd < NN_d[i]):
               ttmpd = NN_d[i]
               ttmpid = NN_id[i]
               NN_d[i] = tmpd
               NN_id[i] = tmpid
               tmpd = ttmpd
               tmpid = ttmpid
     

def main(argv):
     
     # Get input
     cord = argv[2:4]
     k = argv[4]
     con = sqlite3.connect(argv[1])
     cur = con.cursor()       
     cur.execute('PRAGMA foreign_keys = ON;') 
     
     # init
     NN_id = [0] * k
     NN_d = [float('inf')] * k
     
     # Begin the dfs search
     KNN(1)
     
     for i in range(k):
          print("id: "+ str(NN_id[i]) + ", Distance: " + str(NN_d[i]))


if __name__ == "__main__":
     main(sys.argv[0:])
     
     