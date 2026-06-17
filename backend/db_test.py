from db_conn_new import get_oracle_connection

try:
    # Connect to Oracle database
    conn = get_oracle_connection("rundb2")

    # Create cursor
    cursor = conn.cursor()

    # Check how many tables exist for this user
    cursor.execute("SELECT COUNT(*) FROM user_tables")

    count = cursor.fetchone()

    print("Total tables:", count[0])

    # If tables exist, print first 10 table names
    if count[0] > 0:
        cursor.execute("SELECT table_name FROM user_tables")

        rows = cursor.fetchmany(10)

        print("\nFirst 10 tables:")
        for row in rows:
            print(row[0])
    else:
        print("No tables found for this user.")

    # Close resources
    cursor.close()
    conn.close()

    print("\n✅ Query executed successfully.")

except Exception as e:
    print("❌ Error:", e)