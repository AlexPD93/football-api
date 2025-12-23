"""
Login router for the Football API.

Handles routes for the HTML login page.
"""

import os
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

# The router for the dashboard pages
router = APIRouter()

# Templates are configured for this router
templates = Jinja2Templates(directory="templates")


@router.get("/login")
def get_login(request: Request):
    """Renders the login page."""
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login_action(request: Request, password: str = Form(...)):
    """Sends password request to serverless."""
    if password == os.environ.get("ADMIN_PASSWORD"):
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(
            key="admin_access", value="granted", httponly=True, max_age=86400
        )
        return response
    # If it fails, send them back to login with an error message
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": "Incorrect password"}
    )
