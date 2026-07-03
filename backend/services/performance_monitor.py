from db_conn_new import get_oracle_connection

def get_performance(db_name):

    conn = get_oracle_connection(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            name,
            value
        FROM v$sysstat
        WHERE name IN (
            'CPU used by this session',
            'user commits',
            'user rollbacks',
            'parse count (total)',
            'execute count'
        )
    """)

    rows = cursor.fetchall()

    data = []

    for row in rows:
        data.append({
            "metric": row[0],
            "value": row[1]
        })

    cursor.close()
    conn.close()

    return data