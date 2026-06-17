# test_connection.py

from db_conn_new import get_oracle_connection

try:
    conn = get_oracle_connection("rundb1")
    cursor= conn.cursor()
    cursor.execute("SELECT SYSDATE FROM dual")
    for row in cursor:
        print(row)
    cursor.close()
    conn.close()
    print("✅ query executed succesfully")
except Exception as e:
    print("❌ Error:", e)
