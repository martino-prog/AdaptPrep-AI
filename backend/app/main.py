import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db, SessionLocal
from app.seed_data import seed_sample_questions
from app.routers import auth_router, questions_router, submissions_router, analytics_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("[AdaptPrep AI] Initializing Database & Models...")
    init_db()
    
    db = SessionLocal()
    try:
        seed_sample_questions(db)
    finally:
        db.close()
    
    yield
    # Shutdown logic
    print("[AdaptPrep AI] Shutting down application...")

app = FastAPI(
    title="AdaptPrep AI Backend",
    description="Adaptive DSA Practice Platform with AI Code Review and Sandboxed Code Execution",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for React frontend integration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all during dev/demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(auth_router.router)
app.include_router(questions_router.router)
app.include_router(submissions_router.router)
app.include_router(analytics_router.router)

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "online",
        "app": "AdaptPrep AI",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
