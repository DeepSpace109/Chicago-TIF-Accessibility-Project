import pymysql
from table.getTable import getTable
from graphing.makeGraph import graph as bg
from utils.support.exe import exe as ex
from utils.get.cols import cols as col

def row(cursor, tifname,year):

    row = ex(cursor,"SELECT * FROM Chicago_TIF WHERE (tif_name = '{name}' AND tif_year = '{yr}') GROUP BY RAND() LIMIT 1;".format(name=str(tifname),yr=str(year)))
    data = [x for x in row[0]]
    cols = col(cursor)
    print(data)
    retDict = {}
    for idx in range(len(data)):
        retDict[str(cols[idx])] = data[idx]

    return retDict
