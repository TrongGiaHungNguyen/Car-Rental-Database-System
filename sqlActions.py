def modifyData(conn, cur, query, parameters = []):
    try:
        cur.execute(query, parameters)
        conn.commit()
    except Exception as e:
        print(e)