# # # from fastapi import FastAPI

# # # # Import Routers
# # # from api.server_routes import router as server_router
# # # from api.database_routes import router as db_router
# # # from api.session_routes import router as session_router

# # # app = FastAPI(
# # #     title="Enterprise Monitoring Dashboard",
# # #     description="Server and Database Monitoring APIs",
# # #     version="1.0.0"
# # # )

# # # # Register Routes
# # # app.include_router(server_router)
# # # app.include_router(db_router)
# # # app.include_router(session_router)

# # # # Home Route
# # # @app.get("/")
# # # def home():
# # #     return {
# # #         "status": "success",
# # #         "message": "Enterprise Monitoring Backend Running"
# # #     }

# # # # Health Check Route
# # # @app.get("/health")
# # # def health_check():
# # #     return {
# # #         "status": "UP"
# # #     }
# # print("******** THIS IS MAIN.PY ********")
# # from fastapi import FastAPI

# # from api.server_routes import router as server_router
# # from api.database_routes import router as db_router
# # from api.session_routes import router as session_router

# # app = FastAPI(
# #     title="Enterprise Monitoring Dashboard",
# #     description="Server and Database Monitoring APIs",
# #     version="1.0.0"
# # )

# # app.include_router(server_router)
# # app.include_router(db_router)
# # app.include_router(session_router)

# # @app.get("/")
# # def home():
# #     return {"message": "BSP Monitoring Backend Running"}

# # @app.get("/health")
# # def health():
# #     return {"status": "healthy"}
print("MAIN FILE LOADED")
print("IMPORTING ROUTES")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database_routes import router as database_router
from api.session_routes import router as session_router
from api.server_routes import router as server_router
from api.test_routes import router as test_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(database_router)
app.include_router(session_router)
app.include_router(server_router)
app.include_router(test_router)
