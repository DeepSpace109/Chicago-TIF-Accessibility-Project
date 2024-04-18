import pymysql
import csv

#import secure read-only credentials to the database.
#MUST HAVE awscreds.csv EXISTING WITH VALID CREDENTIALS
def connect():
    with open('awscreds.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        
        for row in spamreader:
            creds = (row)
    #TODO Create code to iterate through the read only accounts Nick will create to restrain database usage and regulate it.  
    #establish connection to DB and create cursor.
    try:
        conn = pymysql.connect(
            host=creds[0],
            user=creds[1],
            password=creds[2],
            database="chicago_TIF"
        )
    except pymysql.Error as e:
        print(e)
    return conn




