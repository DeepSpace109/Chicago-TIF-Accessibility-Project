import random as rand
from table.getTable import getTable
from graphing.makeGraph import graph as bg
from utils.support.exe import exe
import numpy as np

def randomSample(cursor):
    n = 30 #random samples

    yeardat = exe(cursor, "SELECT DISTINCT tif_year FROM Chicago_TIF")
    x = []
    for each in yeardat:
        x.append(each[0])

    means = []
    for years in x:
        data = getTable(cursor, "expenses","tif_name","tif_year",str(years))
        means.append((sum([ x[0] for x in data])) / len(data))

    table = list(zip(x,means))

    bg(table,"Years on Record","Random Sample Average Expenditures for that Year ($)","Random Sampled Estimate for Average Expenditures in USD")


    