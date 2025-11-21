"""
Person router endpoints for FastAPI.

Handles GET, POST, PATCH and DELETE operations for person resources.
"""

from fastapi import APIRouter, HTTPException
from actions.person.actions import (
    get_person_by_id_action,
    create_person_action,
    delete_person_action,
    patch_person_action,
)
from .models import Person, CreatePerson, PatchPerson

router = APIRouter(prefix="/person", tags=["person"])

class PersonNotFoundError(Exception):
    """Person not found error"""

class PersonCreationError(Exception):
    """Person creation error"""

class PersonUpdateError(Exception):
    """Person update error"""

class PersonDeleteError(Exception):
    """Person delete error"""

@router.get("/{personId}", response_model=Person)
def get_person(person_id: str):
    """Retrieve a person by ID."""
    try:
        return get_person_by_id_action(person_id)
    except PersonNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Person not found") from exc

@router.post("/", response_model=CreatePerson)
def create_person(person: CreatePerson):
    """Create a new person."""
    try:
        return create_person_action(person).to_domain()
    except PersonCreationError as exc:
        raise HTTPException(status_code=500, detail="Failed to create person") from exc

@router.delete("/{personId}", status_code=204)
def delete_person(person_id: str):
    """Delete a person by ID."""
    try:
        delete_person_action(person_id)
    except PersonNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Person not found") from exc
    except PersonDeleteError as exc:
        raise HTTPException(status_code=500, detail="Failed to delete person") from exc

@router.patch("/{person_id}", response_model=PatchPerson)
def patch_person(person_id: str, person: PatchPerson):
    """Edit a person by ID."""

    try:
        return patch_person_action(person_id, person)
    except PersonNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Person not found") from exc
    except PersonUpdateError as exc:
        raise HTTPException(status_code=500, detail="Failed to update person") from exc
