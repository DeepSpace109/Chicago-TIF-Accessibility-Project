import pymysql
def cols(cursor) -> list | bool:
    try:
        cursor.execute("SHOW COLUMNS FROM Chicago_TIF_Data;")
        results = cursor.fetchall()
        cols = []
        for each in results:
            cols.append(each[0])
        #TODO store in text so as to make this function only run at start time.
        return cols
    except pymysql.Error:
        return False