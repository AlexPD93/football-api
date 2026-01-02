"""
PynamoDB models for Person DynamoDB table.

Defines the PersonModel ORM class and conversion methods between
database and domain (Pydantic) models.
"""

import os
import uuid
from dotenv import load_dotenv
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from routers.person.models import Person, CreatePerson

load_dotenv()


# pylint: disable=too-few-public-methods
class PersonModel(Model):
    """ORM model for Person records in DynamoDB."""

    class Meta:
        """DynamoDB table configuration and AWS credentials."""

        table_name = os.environ["PERSON_TABLE_NAME"]
        region = "eu-west-2"

    PK = UnicodeAttribute(hash_key=True)
    SK = UnicodeAttribute(range_key=True)
    name = UnicodeAttribute(null=True)
    goals_scored = NumberAttribute(null=True)
    games_won = NumberAttribute(null=True)

    def to_domain(self) -> Person:
        """Convert PersonModel (DB) to Person (Pydantic) domain model."""
        data = self.to_simple_dict()
        data["person_id"] = data.pop("PK")
        data.pop("SK", "METADATA")
        return Person.model_validate(data)

    @classmethod
    def from_domain(cls, person_domain: Person | CreatePerson) -> "PersonModel":
        """Convert Person or CreatePerson (Pydantic) to PersonModel (DB)."""
        data = person_domain.model_dump()
        if isinstance(person_domain, CreatePerson):
            data["PK"] = str(uuid.uuid4())
        data["SK"] = "METADATA"
        allowed_keys = set(cls.get_attributes().keys())
        data = {k: v for k, v in data.items() if k in allowed_keys}
        return cls(**data)
