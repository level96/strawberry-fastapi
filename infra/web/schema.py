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
    message: 'Email'

    @strawberry.field(description='This is a description with `print(code)` ')
    async def message(self, root: 'EmailContact', info: Info) -> 'Email':
        emails_loader: DataLoader = info.context.get('emails_loader')
        return await emails_loader.load(root.message_id)


@strawberry.type
class Email:
    id: UUID
    created_at: datetime
    updated_at: datetime
    from_: str
    to: List[str]
    body: str
    contacts: List[EmailContact]

    @strawberry.field(description='This is a description with `print(code)` ')
    async def contacts(self, root: 'Email', info: Info) -> List[EmailContact]:
        contacts_loader: DataLoader = info.context.get('contacts_loader')
        contact_ids_by_email_loader: DataLoader = info.context.get('contact_ids_by_email_loader')

        email_id, contact_ids = await contact_ids_by_email_loader.load(root.id)
        return await contacts_loader.load_many(contact_ids)

    @strawberry.field()
    async def to(self, root: 'Email') -> List[str]:
        return root.to.split(', ')

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
            contacts=[]
        )
