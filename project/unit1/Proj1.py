# Cmput391 Project 1
# Team 20

import xml.etree.ElementTree as ET
import bsddb3 as bsddb
from bsddb3 import db
import random
import os

db = openfile("Proj1.csv","w")
ct = openfile("createDB.sql","w")
def createTable():
     #ct.write("")
    
    
def formatData():
    #db
    
    


def main():
    # Read the XML file
    tree = ET.parse('edmonton.osm')
    root = tree.getroot()
    
    # Create the Database Tables
    createTable()
    
    # Load XML and insert the data
    formatData()
    
    db.close()
    ct.close()
    
main()