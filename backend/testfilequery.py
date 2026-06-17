from db_conn_new import get_oracle_connection
import pandas as pd

try:
    conn = get_oracle_connection("rundb2")

    query = """
    SELECT sys_context('USERENV', 'DB_NAME')
    FROM dual
    """

    cursor = conn.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()

    print("✅ Query executed successfully")

except Exception as e:
    print("error:", e)