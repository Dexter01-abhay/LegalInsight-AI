import os
from pathlib import Path
from dotenv import load_dotenv

# Load environmental layers
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"), encoding="utf-8")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth

# Infrastructure nodes for automated table generation on boot
from backend.database.connection import engine, Base
import backend.database.models

# Create SQL tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LegalInsight AI API", version="1.0.0")

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "LegalInsight AI API Gateway is running."}


@app.get("/health")
def health_check():
    return {"status": "ok"}


# ─── ROUTER REGISTRATION ──────────────────────────────────────────────────
app.include_router(auth.router, tags=["Authentication"])
