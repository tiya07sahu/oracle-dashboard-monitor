from db_conn_new import get_oracle_connection

def get_backup(db_name):

    conn = get_oracle_connection(db_name)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            SESSION_KEY,
            INPUT_TYPE,
            STATUS,
            START_TIME,
            END_TIME
        FROM V$RMAN_BACKUP_JOB_DETAILS
        ORDER BY START_TIME DESC
    """)

    columns = [col[0].lower() for col in cursor.description]

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append(dict(zip(columns, row)))

    cursor.close()
    conn.close()

    return result