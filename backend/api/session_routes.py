# from fastapi import APIRouter

# from services.session_monitor import (
#     get_sessions
# )

# router = APIRouter()

# @router.get("/sessions/{db_name}")
# def session_data(db_name: str):

#     return get_sessions(db_name)
# print("SESSION ROUTES LOADED")
from fastapi import APIRouter
from services.session_monitor import get_sessions

router = APIRouter()

@router.get("/sessions/{db_name}")
def session_data(db_name: str):
    return get_sessions(db_name)
