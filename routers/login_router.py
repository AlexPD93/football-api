"""
Login router for the Football API.

Handles routes for the HTML login page.
"""

import uuid
import time
import os
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from models.session_db import SessionModel

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
        session_token = str(uuid.uuid4())
        expire_timestamp = int(time.time()) + 86400
        new_session = SessionModel(
            session_id=session_token, user_id="admin", expires_at=expire_timestamp
        )
        new_session.save()

        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(
            key="session_id", value=session_token, httponly=True, max_age=86400
        )
        return response
    # If it fails, send them back to login with an error message
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": "Incorrect password"}
    )
