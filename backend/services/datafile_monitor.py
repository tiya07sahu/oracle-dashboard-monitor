from db_conn_new import get_oracle_connection

def get_datafiles(db_name):

    conn = get_oracle_connection(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            file_name,
            tablespace_name,
            ROUND(bytes/1024/1024,2) AS size_mb,
            autoextensible,
            status
        FROM dba_data_files
        ORDER BY tablespace_name
    """)

    rows = cursor.fetchall()

    data = []

    for row in rows:
        data.append({
            "file_name": row[0],
            "tablespace_name": row[1],
            "size_mb": row[2],
            "autoextend": row[3],
            "status": row[4]
        })

    cursor.close()
    conn.close()

    return data