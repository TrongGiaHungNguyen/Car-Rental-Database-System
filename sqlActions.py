def modifyData(conn, cur, query, parameters = []):
    try:
        cur.execute(query, parameters)
        conn.commit()
    except Exception as e:
        print(e)

def fetchAllData(cur, query, parameters=[]):
    try:
        cur.execute(query, parameters)
        return cur.fetchall()  # or use cur.fetchone() if expecting one row
    except Exception as e:
        print(e)
        return None
    
def fetchOneData(cur, query, parameters=[]):
    try:
        cur.execute(query, parameters)
        return cur.fetchone()  # or use cur.fetchone() if expecting one row
    except Exception as e:
        print(e)
        return None
    
