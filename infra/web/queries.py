import logging
import strawberry

from typing import List, Optional, Iterable
from uuid import UUID

from strawberry.types import Info

from infra.storage.models import EmailMessage
from infra.storage.search import EmailSearchRepo
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

    @strawberry.field
    async def search(self, text: str, info: Info) -> List[Email]:
        search_repo: EmailSearchRepo = info.context.get('search_repo')
        return search_repo.search(text)
