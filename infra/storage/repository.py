from uuid import UUID
from dataclasses import dataclass, field
from typing import Optional, Iterable

from core.entities import Email


# from infra.storage.models import EmailMessage


@dataclass
class EmailInMemRepo:
    state: dict = field(default_factory=dict)

    def get(self, pk: UUID) -> Optional[Email]:
        return self.state.get(pk)

    def add(self, obj: Email):
        self.state[obj.id] = obj

    def list(self) -> Iterable[Email]:
        return self.state.values()

# class EmailSQLRepo:
#     def get(self, pk: UUID) -> Optional[Email]:
#         try:
#             return EmailMessage.get(EmailMessage.id == pk)
#         except EmailMessage.DoesNotExist:
#             return None
#
#     def add(self, obj: Email):
#         EmailMessage.create(
#             id=obj.id,
#             created_at=obj.created_at,
#             updated_at=obj.updated_at,
#             from_=obj.from_,
#             to=', '.join(obj.to)
#         )
#
#     def list(self) -> Iterable[Email]:
#         return EmailMessage.select()
