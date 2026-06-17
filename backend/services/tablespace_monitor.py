# # from db_conn_new import get_oracle_connection

# # def get_tablespaces(db_name):

# #     try:

# #         conn = get_oracle_connection(db_name)

# #         cursor = conn.cursor()

# #         cursor.execute("""
# #             SELECT tablespace_name
# #             FROM dba_tablespaces
# #         """)

# #         rows = cursor.fetchall()

# #         result = []

# #         for row in rows:

# #             result.append({
# #                 "tablespace_name": row[0]
# #             })

# #         cursor.close()
# #         conn.close()

# #         return result

# #     except Exception as e:

# #         return {
# #             "error": str(e)
# #         }
# from db_conn_new import get_oracle_connection

# def get_tablespaces(db_name):
#     conn = get_oracle_connection(db_name)
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT tablespace_name,
#                ROUND(used_percent,2)
#         FROM dba_tablespace_usage_metrics
#     """)

#     data = []

#     for row in cursor:
#         data.append({
#             "tablespace": row[0],
#             "used_percent": row[1]
#         })

#     cursor.close()
#     conn.close()

#     return data
# def get_tablespaces(db_name):
#     print("TABLESPACE FUNCTION CALLED")
#     return {
#         "message": "Hello",
#         "db": db_name
#     }
from db_conn_new import get_oracle_connection

def get_tablespaces(db_name):
    conn = get_oracle_connection(db_name)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT tablespace_name
        FROM dba_tablespaces
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows