
from fastapi.middleware.cors import CORSMiddleware
print("MAIN FILE LOADED")
print("IMPORTING ROUTES")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database_routes import router as database_router
from api.session_routes import router as session_router
from api.server_routes import router as server_router
from api.test_routes import router as test_router
from api.datafile_routes import router as datafile_router
from api.storage_routes import router as storage_router
from api.performance_routes import router as performance_router
from api.backup_routes import router as backup_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(database_router)
app.include_router(session_router)
app.include_router(server_router)
app.include_router(test_router)
app.include_router(datafile_router)
app.include_router(storage_router)
app.include_router(performance_router)
app.include_router(backup_router)
