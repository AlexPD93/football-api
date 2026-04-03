"""
Person service for business logic.

Provides functions to create, retrieve, and delete person records from DynamoDB.
"""

import logging
from pynamodb.exceptions import PutError, DeleteError, UpdateError, GetError
from app.models.person_db import PersonModel
from app.schemas.person import Person, CreatePerson, PatchPerson
from app.utils.patch import deep_merge

logger = logging.getLogger(__name__)


class PersonNotFoundError(Exception):
    """Raised when a person is not found in DynamoDB."""

    def __init__(self, person_id: str):
        self.person_id = person_id
        super().__init__(f"Person with ID {person_id} not found.")


class PersonCreationError(Exception):
    """Raised when person creation fails."""

    def __init__(self, message: str = "Failed to create person"):
        super().__init__(message)


class PersonUpdateError(Exception):
    """Raised when person update fails."""

    def __init__(self, person_id: str):
        self.person_id = person_id
        super().__init__(f"Failed to update person {person_id}")


class PersonDeleteError(Exception):
    """Raised when person deletion fails."""

    def __init__(self, person_id: str):
        self.person_id = person_id
        super().__init__(f"Failed to delete person {person_id}")


def get_all_people_action():
    """Scans the DynamoDb table to get all person records."""

    try:
        all_db_persons = PersonModel.scan()
        return [person.to_domain() for person in all_db_persons]
    except GetError as e:
        logger.error("Error scanning table: %s", e)
        return []


def get_person_by_id_action(person_id: str) -> Person:
    """Retrieve a person by ID from DynamoDB."""
    try:
        db_person = PersonModel.get(person_id, "METADATA")
        return db_person.to_domain()
    except PersonModel.DoesNotExist as exc:
        logger.warning("Person not found: %s", person_id)
        raise PersonNotFoundError(person_id) from exc
    except GetError as e:
        logger.error("Error retrieving person %s", person_id, exc_info=True)
        raise PersonNotFoundError(person_id) from e


def create_person_action(create_person: CreatePerson) -> CreatePerson:
    """Create a new person in DynamoDB."""
    try:
        person_model = PersonModel.from_domain(create_person)
        person_model.save()
        logger.info("Person created: %s", person_model.PK)
        return person_model
    except (PutError, ValueError) as e:
        logger.error("Error creating person", exc_info=True)
        raise PersonCreationError("Failed to create person") from e


def delete_person_action(person_id: str) -> bool:
    """Delete a person from DynamoDB by ID."""
    try:
        db_person = PersonModel.get(person_id, "METADATA")
        db_person.delete()
        logger.info("Person deleted: %s", person_id)
        return True
    except PersonModel.DoesNotExist as exc:
        logger.warning("Delete failed – person not found: %s", person_id)
        raise PersonNotFoundError(person_id) from exc
    except DeleteError as e:
        logger.exception("Error deleting person: %s", person_id)
        raise PersonDeleteError(person_id) from e


def patch_person_action(person_id: str, request: PatchPerson) -> PatchPerson:
    """Edit a person from DynamoDB by ID."""
    try:
        db_person = PersonModel.get(person_id, "METADATA")
    except PersonModel.DoesNotExist as exc:
        logger.warning("Patch failed – person not found: %s", person_id)
        raise PersonNotFoundError(person_id) from exc

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
    except UpdateError as e:
        logger.exception("Error updating person: %s", person_id)
        raise PersonUpdateError(person_id) from e


def get_goals_data_action():
    """Returns formatted and sorted data for goals scored."""
    people = get_all_people_action()
    # Convert Pydantic models to dictionaries for easier Jinja2 access
    people_data = [p.model_dump() for p in people]
    return sorted(
        people_data, key=lambda p: p.get("goals_scored", 0) or 0, reverse=True
    )


def get_wins_data_action():
    """Returns formatted and sorted data for games won."""
    people = get_all_people_action()
    # Convert Pydantic models to dictionaries for easier Jinja2 access
    people_data = [p.model_dump() for p in people]
    return sorted(people_data, key=lambda p: p.get("games_won", 0) or 0, reverse=True)
