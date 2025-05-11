from typing import Optional
from pydantic import BaseModel


class ItemIn(BaseModel):
    """Input model for creating or updating items."""
    name: str
    description: Optional[str] = None


class Item(ItemIn):
    """Extended model with ID for database representation."""
    id: int
