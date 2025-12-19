"""
Dashboard router for the Football API.

Handles routes for the HTML dashboard and its components.
"""

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from actions.person.actions import get_goals_data_action, get_wins_data_action

# The router for the dashboard pages
router = APIRouter()

# Templates are configured for this router
templates = Jinja2Templates(directory="templates")


@router.get("/dashboard")
def get_dashboard(request: Request):
    """Renders the main dashboard shell."""
    return templates.TemplateResponse("dashboard.html", {"request": request})


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
