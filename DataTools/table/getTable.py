import pymysql
from utils.support.exe import exe
from scipy.stats import linregress


def getTable(cursor, xaxis,yaxis,sortBy,sortval) -> list | bool :
    """
    takes a cursor object, a variable for the x axis, a variable for the y axis, a constraint variable, and a value for that constraint variable, and returns a table.
    """
    sql = "SELECT DISTINCT {x},{y} FROM Chicago_TIF_Data WHERE {sortVar} = '{sortVal}'".format(sortVar=sortBy, sortVal=sortval, x=xaxis,y=yaxis)

    data = exe(cursor, sql)
    
    returnTable = []
    for idx in range(len(data)):
        returnTable.append([data[idx][0],data[idx][1]])

    if xaxis == "tif_year":
        altTable = sorted(returnTable, key=lambda x: x[0], reverse=False)
        return altTable

    return returnTable
