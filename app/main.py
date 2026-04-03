"""
Football API main application.

FastAPI application entry point that includes modular resource routers.
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from mangum import Mangum
from starlette.middleware.sessions import SessionMiddleware

from app.routers.api.person import router as person_api_router
from app.routers.web.person import router as person_web_router
from app.routers.web.dashboard import router as dashboard_router
from app.routers.web.auth import router as auth_router

app = FastAPI()

app.add_middleware(
    SessionMiddleware, secret_key=os.environ["SECRET_KEY"], max_age=86400
)

# Setup static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"status": "ok"}


# Include the API and Web routers
app.include_router(person_api_router)
app.include_router(person_web_router)
app.include_router(dashboard_router)
app.include_router(auth_router)

handler = Mangum(app)
