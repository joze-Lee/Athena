from fastapi import FastAPI
from app.api import routes
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
# from dotenv import load_dotenv


app = FastAPI()
# load_dotenv() 
app.mount("/static", StaticFiles(directory="frontend"), name="static")

app.include_router(routes.router, prefix="/api")

@app.get("/")
async def read_index():
    return FileResponse(Path("frontend/index.html"))