import logging
import strawberry

from typing import List, Optional
from uuid import UUID

from strawberry.types import Info

from infra.storage.models import EmailMessage
from infra.web.schema import Email

logging.basicConfig(level=logging.DEBUG)


@strawberry.type
class Query:
    @strawberry.field
    async def list_emails(self, info: Info) -> List[Email]:
        return EmailMessage.select()

    @strawberry.field
    async def get_email(self, id: UUID, info: Info) -> Optional[Email]:
        return EmailMessage.select().filter(EmailMessage.id == id)
