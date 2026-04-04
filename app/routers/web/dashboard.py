"""
Dashboard router for the Football API.

Handles routes for the main HTML dashboard shell.
"""

import os
from typing import Optional
from fastapi import APIRouter, Depends, Request, Query
from fastapi.templating import Jinja2Templates

# The router for the dashboard pages
router = APIRouter(tags=["dashboard"])

# Templates are configured for this router
templates = Jinja2Templates(directory="app/templates")


def get_admin_user(request: Request):
    """
    Checks the session to see if the user is a whitelisted admin.
    Returns: 'admin' or 'guest'
    """
    email = request.session.get("user")
    if not email:
        return "guest"

    whitelist = os.environ.get("ADMIN_WHITELIST", "").split(",")
    if email in whitelist:
        return "admin"


@router.get("/dashboard")
def get_dashboard(
    request: Request,
    role: str = Depends(get_admin_user),
    error: Optional[str] = Query(None),
):
    """Renders the main dashboard shell."""
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "role": role, "error_message": error},
    )
