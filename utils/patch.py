"""
Utility functions for merging and patching data structures.

Provides deep merge functionality to combine request updates with database objects.
"""

from typing import Any, Dict

def _to_dict(obj: Any) -> Dict[str, Any]:
    """Convert various object types to a plain dict."""
    if obj is None:
        return {}
    # PynamoDB model
    if hasattr(obj, "to_simple_dict"):
        return obj.to_simple_dict()
    # Pydantic v2
    if hasattr(obj, "model_dump"):
        try:
            return obj.model_dump(exclude_unset=True)
        except TypeError:
            return obj.model_dump()
    # Pydantic v1
    if hasattr(obj, "dict"):
        try:
            return obj.dict(exclude_unset=True)
        except TypeError:
            return obj.dict()
    # already a dict
    if isinstance(obj, dict):
        return dict(obj)
    return {}

def _recursive_merge(base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge updates into base. Skip None values in updates."""
    for k, v in updates.items():
        if v is None:
            # do not overwrite with explicit None
            continue
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            base[k] = _recursive_merge(dict(base.get(k)), v)
        else:
            base[k] = v
    return base

def deep_merge(database, request) -> Dict[str, Any]:
    """Merge `request` into `database` and return the merged dict.

    - Normalizes input (Pydantic models, PynamoDB models, dicts, or objects).
    - Performs a recursive merge for nested dicts.
    - Does not overwrite fields with None from the request.
    """
    base = _to_dict(database)
    updates = _to_dict(request)

    if not updates:
        return base

    return _recursive_merge(base, updates)
