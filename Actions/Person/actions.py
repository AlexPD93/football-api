"""
Person action handlers for business logic.

Provides functions to create, retrieve, and delete person records from DynamoDB.
"""
from pynamodb.exceptions import PutError, DeleteError, UpdateError
from Routers.Person.models_db import PersonModel
from Routers.Person.models import (Person, CreatePerson, PatchPerson)
from utils import deep_merge

def get_person_by_id_action(person_id: str) -> Person:
    """Retrieve a person by ID from DynamoDB."""
    try:
        db_person = PersonModel.get(person_id, "METADATA")
        return db_person.to_domain()
    except PersonModel.DoesNotExist:
        return None

def create_person_action(create_person: CreatePerson) -> CreatePerson:
    """Create a new person in DynamoDB."""
    try:
        person_model = PersonModel.from_domain(create_person)
        person_model.save()
        return person_model
    except (PutError, ValueError) as e:
        print("Error creating person", e)
        return None

def delete_person_action(person_id: str) -> bool:
    """Delete a person from DynamoDB by ID."""
    try:
        db_person = PersonModel.get(person_id, "METADATA")
        db_person.delete()
        return True
    except (DeleteError, PersonModel.DoesNotExist) as e:
        print("Error deleting person", e)
        return False

def patch_person_action(person_id: str, request: PatchPerson) -> PatchPerson:
    """Edit a person from DynamoDB by ID."""
    try:
        db_person = PersonModel.get(person_id, "METADATA")
    except PersonModel.DoesNotExist:
        return None

    # merge request updates into db_person
    patched_dict = deep_merge(db_person, request)

    # apply merged values back to the model (skip PK/SK)
    for k, v in patched_dict.items():
        if k not in ("PK", "SK"):
            setattr(db_person, k, v)

    # save the updated model
    try:
        db_person.save()
        return db_person
    except UpdateError as e:
        print("Error updating person", e)
        return None
