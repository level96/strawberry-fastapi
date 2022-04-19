from typing import List
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class BaseEntity:
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Message(BaseEntity):
    from_: str = None
    to: List[str] = field(default_factory=list)
    body: str = None


@dataclass
class Email(BaseEntity):
    from_: str = None
    to: List[str] = field(default_factory=list)
    body: str = None
