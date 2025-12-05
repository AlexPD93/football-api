"""
Football API main application.

FastAPI application entry point that includes person resource routers.
"""

from fastapi import FastAPI
from routers.person import user_router

app = FastAPI()

@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"status": "ok"}

app.include_router(user_router.router)
