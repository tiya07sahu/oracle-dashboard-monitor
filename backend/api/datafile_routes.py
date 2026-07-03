from fastapi import APIRouter
from services.datafile_monitor import get_datafiles

router = APIRouter()

@router.get("/datafiles/{db_name}")
def datafiles(db_name: str):
    return get_datafiles(db_name)