from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import upload, planning, chat, export, history

app = FastAPI(
    title="AI Restaurant Planning",
    description="Automatic employee work hour scheduling for restaurants",
    version="1.0.0",
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(planning.router, prefix="/api/planning", tags=["planning"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(export.router, prefix="/api/export", tags=["export"])
app.include_router(history.router, prefix="/api/history", tags=["history"])


@app.get("/")
async def root():
    return {"message": "AI Restaurant Planning API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
