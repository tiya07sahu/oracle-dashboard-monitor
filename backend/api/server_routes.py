# # api/server_routes.py

# from fastapi import APIRouter
# from services.server_monitor import get_server_health

# router = APIRouter()

# @router.get("/servers")
# def get_servers():
#     return get_server_health()
from fastapi import APIRouter
from services.server_monitor import get_server_health

router = APIRouter()

@router.get("/servers")
def server_data():
    return get_server_health()