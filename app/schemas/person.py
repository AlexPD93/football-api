"""
Pydantic models for Person API requests and responses.

Defines schemas for creating, retrieving, and updating person records.
"""

from typing import Optional
from pydantic import BaseModel

class Person(BaseModel):
    """Response model for a person record."""
    person_id: str
    name: str
    goals_scored: int
    games_won: int

class CreatePerson(BaseModel):
    """Request model for creating a new person."""
    name: str
    goals_scored: Optional[int] = 0
    games_won: Optional[int] = 0

class PatchPerson(BaseModel):
    """Request model for partially updating a person."""
    name: Optional[str] = None
    goals_scored: Optional[int] = None
    games_won: Optional[int] = None
