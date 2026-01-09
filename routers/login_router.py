"""
Login router for the Football API.

Handles routes for the HTML login page.
"""

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

# The router for the dashboard pages
router = APIRouter()

# Templates are configured for this router
templates = Jinja2Templates(directory="templates")


@router.get("/login")
def get_login(request: Request):
    """Renders the login page."""
    return templates.TemplateResponse("login.html", {"request": request})
