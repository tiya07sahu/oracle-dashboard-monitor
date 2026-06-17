# from db_conn_new import get_oracle_connection

# SESSION_QUERY = """
# SELECT
# username,
# status
# FROM v$session
# WHERE username IS NOT NULL
# """

# def get_sessions(db_name):

#     try:

#         conn = get_oracle_connection(db_name)

#         cursor = conn.cursor()

#         cursor.execute(SESSION_QUERY)

#         columns = [col[0] for col in cursor.description]

#         rows = cursor.fetchall()

#         result = []

#         for row in rows:

#             result.append(
#                 dict(zip(columns, row))
#             )

#         cursor.close()
#         conn.close()

#         return result

#     except Exception as e:

#         return {
#             "error": str(e)
#         }
# from db_conn_new import get_oracle_connection

# def get_sessions(db_name):
#     print("SESSION FUNCTION CALLED")
#     conn = get_oracle_connection(db_name)
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT username,
#                status,
#                machine
#         FROM v$session
#         WHERE username IS NOT NULL
#     """)

#     sessions = []

#     for row in cursor:
#         sessions.append({
#             "username": row[0],
#             "status": row[1],
#             "machine": row[2]
#         })

#     cursor.close()
#     conn.close()

#     return sessions
from db_conn_new import get_oracle_connection

def get_sessions(db_name):
    print("STEP 1")

    conn = get_oracle_connection(db_name)
    print("STEP 2")

    cursor = conn.cursor()
    print("STEP 3")

    cursor.execute("""
        SELECT username,
               status,
               machine
        FROM v$session
        WHERE username IS NOT NULL
    """)
    print("STEP 4")

    rows = cursor.fetchall()
    print("STEP 5")

    return rows