from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class Message(BaseModel):
    message: str


class RequestUser(BaseModel):
    name: str = Field(..., examples=["senya"])
    email: str = Field(..., examples=["senya@example.com"])
    age: int = Field(..., examples=[69])


class User(RequestUser):
    id: Optional[int] = None
    created_at: Optional[datetime] = None


class Page(BaseModel):
    items: List[User]
    hasMore: bool
