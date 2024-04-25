import random as rand
from table.getTable import getTable
from graphing.makeGraph import graph as bg
from utils.support.exe import exe
import numpy as np
from utils.get.row import row as r

def investmentQuality(cursor,tifname,firstPartition=False):

    boundry1=13612.06
    boundry2=359447.2

    data = []

    if firstPartition == False:
        for x in range(2012,2023):
            try:
                temp = r(cursor, tifname,x)
                data.append(temp['expenses'])
            except:
                pass
            
    else:
        for x in range(2002,2013):
            try:
                temp = r(cursor, tifname,x)
                data.append(temp['expenses'])
            except:
                pass

    x = sum(data) / len(data)
    
    match x:
        case _ if x < boundry1:
            return "Low"
        case _ if x > boundry1 and x < boundry2:
            return "Medium"
        case _:
            return "High"
