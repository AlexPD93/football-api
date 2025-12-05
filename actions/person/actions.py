"""
Person action handlers for business logic.

Provides functions to create, retrieve, and delete person records from DynamoDB.
"""
import logging
from pynamodb.exceptions import PutError, DeleteError, UpdateError, GetError
from routers.person.models_db import PersonModel
from routers.person.models import (Person, CreatePerson, PatchPerson)
from utils import deep_merge

logger = logging.getLogger(__name__)

def get_all_people_action():
    """Scans the DynamoDb table to get all person records."""

    try:
        all_db_persons = PersonModel.scan()
        return [person.to_domain() for person in all_db_persons]
    except GetError:
        logger.error("Error scanning table: {e}")
        return []

def get_person_by_id_action(person_id: str) -> Person:
    """Retrieve a person by ID from DynamoDB."""
    try:
        db_person = PersonModel.get(person_id, "METADATA")
        return db_person.to_domain()
    except PersonModel.DoesNotExist:
        logger.warning("Person not found: %s", person_id)
        return None
    except GetError:
        logger.error("Error retrieving person %s", person_id, exc_info=True)
        return None

def create_person_action(create_person: CreatePerson) -> CreatePerson:
    """Create a new person in DynamoDB."""
    try:
        person_model = PersonModel.from_domain(create_person)
        person_model.save()
        logger.info("Person created: %s", person_model.PK)
        return person_model
    except (PutError, ValueError):
        logger.error("Error creating person", exc_info=True)
        return None

def delete_person_action(person_id: str) -> bool:
    """Delete a person from DynamoDB by ID."""
    try:
        db_person = PersonModel.get(person_id, "METADATA")
        db_person.delete()
        logger.info("Person deleted: %s", person_id)
        return True
    except PersonModel.DoesNotExist:
        logger.warning("Delete failed – person not found: %s", person_id)
        return False
    except DeleteError:
        logger.exception("Error deleting person: %s", person_id)
        return False

def patch_person_action(person_id: str, request: PatchPerson) -> PatchPerson:
    """Edit a person from DynamoDB by ID."""
    try:
        db_person = PersonModel.get(person_id, "METADATA")
    except PersonModel.DoesNotExist:
        logger.warning("Patch failed – person not found: %s", person_id)
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
        logger.info("Person updated: %s", person_id)
        return db_person
    except UpdateError:
        logger.exception("Error updating person: %s", person_id)
        return None
