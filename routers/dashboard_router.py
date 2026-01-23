"""
Dashboard router for the Football API.

Handles routes for the HTML dashboard and its components.
"""

import os
from typing import Optional
from fastapi import APIRouter, Depends, Request, Query
from fastapi.templating import Jinja2Templates
from actions.person.actions import get_goals_data_action, get_wins_data_action

# The router for the dashboard pages
router = APIRouter()

# Templates are configured for this router
templates = Jinja2Templates(directory="templates")


def get_admin_user(request: Request):
    """
    Checks the session to see if the user is a whitelisted admin.
    Returns: 'admin', 'guest', or None.
    """
    email = request.session.get("user")
    if not email:
        return "guest"

    whitelist = os.environ.get("ADMIN_WHITELIST", "").split(",")
    if email in whitelist:
        return "admin"

    return "guest"


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


@router.get("/goals")
def get_goals(request: Request):
    """Returns HTML fragment for goals scored."""
    context = {
        "request": request,
        "rows": get_goals_data_action(),
        "headers": ["Player", "Goals"],
        "fields": ["name", "goals_scored"],
    }
    return templates.TemplateResponse("partials/_table.html", context)


@router.get("/wins")
def get_wins(request: Request):
    """Returns HTML fragment for games won."""
    context = {
        "request": request,
        "rows": get_wins_data_action(),
        "headers": ["Player", "Wins"],
        "fields": ["name", "games_won"],
    }
    return templates.TemplateResponse("partials/_table.html", context)
