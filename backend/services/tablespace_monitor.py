from db_conn_new import get_oracle_connection

def get_tablespaces(db_name):

    conn = get_oracle_connection(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            df.tablespace_name,
            ROUND(SUM(df.bytes)/1024/1024,2) allocated_mb,
            ROUND(NVL(fs.free_mb,0),2) free_mb
        FROM dba_data_files df
        LEFT JOIN
        (
            SELECT
                tablespace_name,
                SUM(bytes)/1024/1024 free_mb
            FROM dba_free_space
            GROUP BY tablespace_name
        ) fs
        ON df.tablespace_name = fs.tablespace_name
        GROUP BY
            df.tablespace_name,
            fs.free_mb
        ORDER BY
            df.tablespace_name
    """)

    rows = cursor.fetchall()

    data = []

    for row in rows:

        tablespace = row[0]
        allocated = float(row[1] or 0)
        free = float(row[2] or 0)

        used = allocated - free

        percent_used = 0 if allocated == 0 else round((used / allocated) * 100,2)
        percent_free = 100 - percent_used

        if percent_used >= 90:
            status = "Critical"
        elif percent_used >= 75:
            status = "Warning"
        else:
            status = "Healthy"

        data.append({

            "tablespace_name": tablespace,

            "max_mb": allocated,

            "allocated_mb": allocated,

            "free_mb": free,

            "used_mb": round(used,2),

            "percentage_used": percent_used,

            "available_extension_mb": round(free,2),

            "percentage_free": round(percent_free,2),

            "status": status

        })

    cursor.close()
    conn.close()

    return data