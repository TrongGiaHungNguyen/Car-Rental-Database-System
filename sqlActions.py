def modifyData(conn, cur, query, parameters = []):
    try:
        cur.execute(query, parameters)
        conn.commit()
        print("Success!")
    except Exception as e:
        print("__ERROR__:", e)
        conn.rollback()

def fetchAllData(cur, query, parameters=[]):
    try:
        cur.execute(query, parameters)
        returnVal = cur.fetchall()
        print("Success!")
        return returnVal
    except Exception as e:
        print("__ERROR__:", e)
        return None
    
def fetchOneData(cur, query, parameters=[]):
    try:
        cur.execute(query, parameters)
        returnVal = cur.fetchone()
        return returnVal
    except Exception as e:
        print("__ERROR__:", e)
        return None
    
