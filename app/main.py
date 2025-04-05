from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routes import users, websocket
from .db import engine, Base
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env", override=True)
import os

app = FastAPI()

app.include_router(users.router)
app.include_router(websocket.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

# For production, allowed origins should be set
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ For dev only: allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    # Create the database tables if they don't exist
    if os.getenv("TESTING"):
        return
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_root():
    return {"Hello": "World"}