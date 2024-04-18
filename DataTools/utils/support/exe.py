import pymysql

def exe(cursor,query):
    try:
        cursor.execute(query)
        data = cursor.fetchall()
    except pymysql.Error as e:
        print(e)
        return False
    
    return data