"""
Person router endpoints for FastAPI.

Handles GET, POST, PATCH and DELETE operations for person resources.
"""

from fastapi import APIRouter, HTTPException
from app.services.person_service import (
    get_all_people_action,
    get_person_by_id_action,
    create_person_action,
    delete_person_action,
    patch_person_action,
    PersonNotFoundError,
    PersonCreationError,
    PersonUpdateError,
    PersonDeleteError,
)
from app.schemas.person import Person, CreatePerson, PatchPerson

router = APIRouter(prefix="/person", tags=["person"])


@router.get("/", response_model=list[Person])
def get_all_persons():
    """Retrieve all persons."""
    return get_all_people_action()


@router.get("/{person_id}", response_model=Person)
def get_person(person_id: str):
    """Retrieve a person by ID."""
    try:
        return get_person_by_id_action(person_id)
    except PersonNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.post("/", response_model=Person)
def create_person(person: CreatePerson):
    """Create a new person."""
    try:
        person_model = create_person_action(person)
        return person_model.to_domain()
    except PersonCreationError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.delete("/{person_id}", status_code=204)
def delete_person(person_id: str):
    """Delete a person by ID."""
    try:
        delete_person_action(person_id)
    except PersonNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PersonDeleteError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@router.patch("/{person_id}", response_model=Person)
def patch_person(person_id: str, person: PatchPerson):
    """Edit a person by ID."""
    try:
        person_model = patch_person_action(person_id, person)
        return person_model.to_domain()
    except PersonNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PersonUpdateError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal server error") from exc
