from fastapi import APIRouter

from services.tablespace_monitor import (
    get_tablespaces
)

router = APIRouter()

@router.get("/tablespaces/{db_name}")
def tablespace_data(db_name: str):

    return get_tablespaces(db_name)
# # from fastapi import APIRouter
# # from services.tablespace_monitor import get_tablespaces

# # router = APIRouter()

# # @router.get("/tablespaces/{db_name}")
# # def tablespace_data(db_name: str):
# #     return get_tablespaces(db_name)

# from fastapi import APIRouter
# from services.tablespace_monitor import get_tablespaces

# print("DATABASE ROUTES FILE LOADED")

# router = APIRouter()

# @router.get("/tablespaces/{db_name}")
# def tablespace_data(db_name: str):
#     print("TABLESPACE ROUTE HIT")
#     return get_tablespaces(db_name)
# from fastapi import APIRouter

# router = APIRouter()

# @router.get("/tablespaces/{db_name}")
# def tablespace_data(db_name: str):
#     print("Endpoint hit!")
#     return {
#         "message": "API working",
#         "database": db_name
#     }