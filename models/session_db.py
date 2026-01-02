"""
PynamoDB models for Session DynamoDB table.

Defines the SessionModel ORM class and conversion methods between
database and domain (Pydantic) models.
"""

import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute


class SessionModel(Model):
    """ORM model for Session records in DynamoDB."""

    class Meta:
        """DynamoDB table configuration and AWS credentials."""

    table_name = os.environ["SESSION_TABLE_NAME"]
    region = "eu-west-2"

    session_id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute()
    expires_at = NumberAttribute()  # This will be our TTL attribute
