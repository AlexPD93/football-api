"""
Dashboard router for the Football API.

Handles routes for the HTML dashboard and its components.
"""

import os
from typing import Optional
from fastapi import APIRouter, Depends, Request, Query
from fastapi.templating import Jinja2Templates
from routers.person.models import PatchPerson
from routers.person.models import CreatePerson
from actions.person.actions import (
    get_goals_data_action,
    get_wins_data_action,
    get_person_by_id_action,
    create_person_action,
    delete_person_action,
    patch_person_action,
)

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
def get_goals(request: Request, role: str = Depends(get_admin_user)):
    """Returns HTML fragment for goals scored."""
    context = {
        "request": request,
        "rows": get_goals_data_action(),
        "headers": ["Player", "Goals"],
        "fields": ["name", "goals_scored"],
        "role": role,
        "table_type": "goals",
    }
    return templates.TemplateResponse("partials/_table.html", context)


@router.get("/wins")
def get_wins(request: Request, role: str = Depends(get_admin_user)):
    """Returns HTML fragment for games won."""
    context = {
        "request": request,
        "rows": get_wins_data_action(),
        "headers": ["Player", "Wins"],
        "fields": ["name", "games_won"],
        "role": role,
        "table_type": "wins",
    }
    return templates.TemplateResponse("partials/_table.html", context)


@router.get("/edit/{person_id}")
def edit_person(
    request: Request,
    person_id: str,
    table_type: str,
    role: str = Depends(get_admin_user),
):
    """Returns the edit row partial."""
    person = get_person_by_id_action(person_id)
    if not person:
        return "Person not found"

    context = {
        "request": request,
        "row": person.model_dump(),
        "fields": (
            ["name", "goals_scored"] if table_type == "goals" else ["name", "games_won"]
        ),
        "role": role,
        "table_type": table_type,
    }

    if role != "admin":
        return templates.TemplateResponse("partials/_table_row.html", context)

    return templates.TemplateResponse("partials/_edit_row.html", context)


@router.put("/actions/{field}/{action}/{person_id}")
async def update_count(
    request: Request,
    field: str,
    action: str,
    person_id: str,
    table_type: str,
    role: str = Depends(get_admin_user),
):
    """Increments or decrements a field value based on current UI input and returns the edit row."""

    if role != "admin":
        return "Unauthorized"

    form_data = await request.form()
    person = get_person_by_id_action(person_id)
    if not person:
        return "Person not found"

    person_dict = person.model_dump()

    try:
        # Priority: form_data > db
        current_val = int(form_data.get(field, person_dict.get(field, 0)))
    except (ValueError, TypeError):
        current_val = person_dict.get(field, 0)

    if action == "increment":
        person_dict[field] = current_val + 1
    else:
        person_dict[field] = max(0, current_val - 1)

    # Note: Returns ONLY the edit row partial
    context = {
        "request": request,
        "row": person_dict,
        "fields": (
            ["name", "goals_scored"] if table_type == "goals" else ["name", "games_won"]
        ),
        "role": role,
        "table_type": table_type,
    }
    return templates.TemplateResponse("partials/_edit_row.html", context)


@router.put("/save/{person_id}")
async def save_person(
    request: Request,
    person_id: str,
    table_type: str,
    role: str = Depends(get_admin_user),
):
    """Persists changes and returns the full sorted table."""

    if role != "admin":
        return "Unauthorized"

    form_data = await request.form()
    update_data = {}
    for field in ["goals_scored", "games_won"]:
        if field in form_data:
            try:
                update_data[field] = int(form_data[field])
            except ValueError:
                pass

    if update_data:
        patch_person_action(person_id, PatchPerson(**update_data))

    # Return the full table sorted
    if table_type == "goals":
        rows = get_goals_data_action()
        headers = ["Player", "Goals"]
        fields = ["name", "goals_scored"]
    else:
        rows = get_wins_data_action()
        headers = ["Player", "Wins"]
        fields = ["name", "games_won"]

    context = {
        "request": request,
        "rows": rows,
        "headers": headers,
        "fields": fields,
        "role": role,
        "table_type": table_type,
    }
    return templates.TemplateResponse("partials/_table.html", context)


@router.get("/new-player-modal")
def get_new_player_modal(
    request: Request, table_type: str, role: str = Depends(get_admin_user)
):
    """Returns the modal content for adding a new player."""
    if role != "admin":
        return "Unauthorized"
    return templates.TemplateResponse(
        "partials/_player_modal.html", {"request": request, "table_type": table_type}
    )


@router.post("/save/new")
async def save_new_person(
    request: Request,
    role: str = Depends(get_admin_user),
):
    """Creates a new player and returns the full sorted table."""

    if role != "admin":
        return "Unauthorized"

    form_data = await request.form()
    table_type = form_data.get("table_type", "goals")

    new_person_data = CreatePerson(
        name=form_data.get("name", "Unknown Player"),
        goals_scored=int(form_data.get("goals_scored", 0)),
        games_won=int(form_data.get("games_won", 0)),
    )

    create_person_action(new_person_data)

    # Return the full table sorted
    if table_type == "goals":
        rows = get_goals_data_action()
        headers = ["Player", "Goals"]
        fields = ["name", "goals_scored"]
    else:
        rows = get_wins_data_action()
        headers = ["Player", "Wins"]
        fields = ["name", "games_won"]

    context = {
        "request": request,
        "rows": rows,
        "headers": headers,
        "fields": fields,
        "role": role,
        "table_type": table_type,
    }
    return templates.TemplateResponse("partials/_table.html", context)


@router.delete("/delete/{person_id}")
def delete_player(
    person_id: str,
    role: str = Depends(get_admin_user),
):
    """Deletes a player and returns an empty response to remove the row from the UI."""

    if role != "admin":
        return "Unauthorized"

    delete_person_action(person_id)
    return ""


@router.get("/cancel/{person_id}")
def cancel_edit(
    request: Request,
    person_id: str,
    table_type: str,
    role: str = Depends(get_admin_user),
):
    """Returns the normal table row, discarding unsaved changes."""

    person = get_person_by_id_action(person_id)
    context = {
        "request": request,
        "row": person.model_dump(),
        "fields": (
            ["name", "goals_scored"] if table_type == "goals" else ["name", "games_won"]
        ),
        "role": role,
        "table_type": table_type,
    }
    return templates.TemplateResponse("partials/_table_row.html", context)
