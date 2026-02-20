import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.exceptions import http_exception_handler
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="HRMS Lite API")

# Create tables ONLY in local/dev
if os.getenv("ENV") != "production":
    Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "HRMS Lite Backend Running"}