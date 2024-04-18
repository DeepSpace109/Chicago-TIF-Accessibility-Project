import pandas as pd
import pymysql
import csv
from establishConnection import connect as cn
from utils.get.cols import cols
from table.getTable import getTable as tab
from graphing.makeGraph import graph as g
from utils.get.netIncome import netIncomeByYear
from utils.support.exe import exe as ex
from utils.get.row import row
from utils.get.avggrowth import avggrowth as ag

#Chicago_TIF capital C
"SELECT * FROM Chicago_TIF WHERE tif_name = '35th/Halsted';"

#startup - create network connection and required cursor
conn = cn()
cursor = conn.cursor()

#startup queries
#TODO write these names to file so as to not need to query database for this info again

# data = tab(cursor,'tif_year','cumulative_property_tax_extraction','tif_name',"35th/Halsted")


ret = ex(cursor, "SELECT DISTINCT tif_name FROM Chicago_TIF")

tifNames = [x[0] for x in ret]
print (tifNames)

# g(data)

datatab = tab(cursor,'tif_year','property_tax_extraction','tif_name',"35th/Halsted")
print(datatab)

# print(ex(cursor, "SELECT DISTINCT start_year FROM Chicago_TIF WHERE tif_name = '35th/Halsted';"))

# ret = row(cursor,'35th/Halsted',2021)

print(ag(datatab))








#close everything off
cursor.close()
conn.commit()
conn.close()