"""
Football API main application.

FastAPI application entry point that includes person resource routers.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from mangum import Mangum

from routers.person.person_router import router as person_router
from routers.dashboard_router import router as dashboard_router

app = FastAPI()

# Setup static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"status": "ok"}


# Include the API and dashboard routers
app.include_router(person_router)
app.include_router(dashboard_router)

handler = Mangum(app)
