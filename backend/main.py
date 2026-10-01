import os
import threading
from pathlib import Path
from dotenv import load_dotenv

# Load environmental layers
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"), encoding="utf-8")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth, upload

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
app.include_router(upload.router, prefix="/api", tags=["Documents"])


# ─── OPTIONAL BACKGROUND AI PRELOADING ──────────────────────────────────────

def preload_model():
    try:
        print("[startup] Loading ML model in background...")
        from backend.pipelines.contract_analyzer import get_model
        get_model()
        print("[startup] ML model ready.")
    except Exception as e:
        print(f"[startup] Model preload failed: {e}")


if os.getenv("ENABLE_MODEL_PRELOAD", "false").lower() == "true":
    threading.Thread(target=preload_model, daemon=True).start()
