"""
Person router endpoints for FastAPI.

Handles GET, POST, and DELETE operations for person resources.
"""

from fastapi import APIRouter, HTTPException
from Actions.Person.actions import (
    get_person_by_id_action,
    create_person_action,
    delete_person_action,
    patch_person_action,
)
from .models import Person, CreatePerson, PatchPerson

router = APIRouter(prefix="/person", tags=["person"])

@router.get("/{personId}", response_model=Person)
def get_person(person_id: str):
    """Retrieve a person by ID."""
    person = get_person_by_id_action(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@router.post("/", response_model=CreatePerson)
def create_person(person: CreatePerson):
    """Create a new person."""
    person = create_person_action(person)

    if not person:
        raise HTTPException(status_code=500, detail="Error creating person")
    return person.to_domain()

@router.delete("/{personId}", status_code=204)
def delete_person(person_id: str):
    """Delete a person by ID."""
    success = delete_person_action(person_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

@router.patch("/{person_id}", response_model=PatchPerson)
def patch_person(person_id: str, person: PatchPerson):
    """Edit a person by ID."""

    person = patch_person_action(person_id, person)

    if not person:
        raise HTTPException(status_code=500, detail="Error editing person")
    return person
