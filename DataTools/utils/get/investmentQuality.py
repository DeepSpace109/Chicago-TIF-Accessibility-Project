import random as rand
from table.getTable import getTable
from graphing.makeGraph import graph as bg
from utils.support.exe import exe
import numpy as np


def investmentQuality(cursor,tifname, boundry1, boundry2):

    tab = getTable(cursor,'expenses','transfers_out','tif_name',tifname)

    temp = []

    for exp,trans in tab:
        temp.append(exp - trans)

    x = sum(temp)
    
    match x:
        case _ if x < boundry1:
            return "Low"
        case _ if x > boundry1 and x < boundry2:
            return "Medium"
        case _:
            return "High"
