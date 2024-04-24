import pandas as pd
import pymysql
import csv
from establishConnection import connect as cn
from utils.get.cols import cols
from table.getTable import getTable as tab
from graphing.makeGraph import graph as g
from utils.get.netIncome import netIncomeByYear as net
from utils.support.exe import exe as ex
from utils.get.row import row
from utils.get.avggrowth import avggrowth as ag
from utils.get.investmentQuality import investmentQuality as iq
from utils.get.randomsample import randomSample as rs

#Chicago_TIF capital C
"SELECT * FROM Chicago_TIF WHERE tif_name = '35th/Halsted';"

#startup - create network connection and required cursor
conn = cn()
cursor = conn.cursor()

#startup queries
#TODO write these names to file so as to not need to query database for this info again

# data = tab(cursor,'tif_year','cumulative_property_tax_extraction','tif_name',"35th/Halsted")


# ret = ex(cursor, "SELECT DISTINCT tif_name FROM Chicago_TIF")

# print(cols(cursor))

# rs(cursor)

print(iq(cursor, "35th/Halsted",5000000000, 15000000000))





#close everything off
cursor.close()
conn.commit()
conn.close()