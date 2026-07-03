from fastapi import APIRouter
from services.storage_monitor import get_storage

router = APIRouter()

@router.get("/storage/{db_name}")
def storage(db_name: str):
    return get_storage(db_name)