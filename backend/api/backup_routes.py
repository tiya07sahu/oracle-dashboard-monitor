from fastapi import APIRouter
from services.backup_monitor import get_backup

router = APIRouter()

@router.get("/backup/{db_name}")
def backup_data(db_name: str):
    return get_backup(db_name)