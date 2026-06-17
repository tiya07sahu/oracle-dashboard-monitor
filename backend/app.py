from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "BSP Monitoring Backend Running"}