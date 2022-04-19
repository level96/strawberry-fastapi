import strawberry

from typing import List, Optional
from datetime import datetime
from uuid import UUID
from strawberry.dataloader import DataLoader
from strawberry.types import Info


@strawberry.type
class Message:
    id: UUID
    created_at: datetime
    updated_at: datetime
    from_: str
    to: List[str]
    body: str

    @classmethod
    def from_dict(cls, data) -> 'Email':
        return cls(
            id=UUID(data['id']),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            from_=data['from_'],
            to=data['to'],
            body=data['body'],
        )


@strawberry.type
class EmailContact:
    id: UUID
    created_at: datetime
    updated_at: datetime
    first_name: str
    last_name: str
    email: str


@strawberry.type
class Email:
    id: UUID
    created_at: datetime
    updated_at: datetime
    from_: str
    to: List[str]
    contacts: List[EmailContact]
    body: str

    @strawberry.field(description='This is a description with `print(code)` ')
    async def contacts(self, root: 'Email', info: Info) -> List[EmailContact]:
        contacts_loader: DataLoader = info.context.get('contacts_loader')
        contact_ids_by_email_loader: DataLoader = info.context.get('contact_ids_by_email_loader')

        email_id, contact_ids = await contact_ids_by_email_loader.load(root.id)
        valid_ids = filter(lambda x: bool(x), contact_ids)
        return await contacts_loader.load_many(valid_ids)

    @strawberry.field(deprecation_reason='outdated in favor for xxx')
    async def deprecated(self) -> Optional[str]:
        return None

    @classmethod
    def from_dict(cls, data) -> 'Email':
        return cls(
            id=UUID(data['id']),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            from_=data['from_'],
            to=data['to'],
            body=data['body'],
        )
