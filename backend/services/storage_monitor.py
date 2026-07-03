from db_conn_new import get_oracle_connection

def get_storage(db_name):

    conn = get_oracle_connection(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            tablespace_name,
            ROUND(SUM(bytes)/1024/1024,2) AS total_mb
        FROM dba_data_files
        GROUP BY tablespace_name
        ORDER BY total_mb DESC
    """)

    rows = cursor.fetchall()

    data = []

    for row in rows:
        data.append({
            "tablespace_name": row[0],
            "size_mb": row[1]
        })

    cursor.close()
    conn.close()

    return data