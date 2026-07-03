from fastapi import APIRouter
from services.performance_monitor import get_performance

router = APIRouter()

@router.get("/performance/{db_name}")
def performance(db_name: str):
    return get_performance(db_name)