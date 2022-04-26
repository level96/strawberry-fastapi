import random
import strawberry

from faker import Faker
from typing import List
from strawberry.types import Info

from core.entities import Email as EmailEntity
from infra.messaging.provider import MessageProvider
from infra.storage.models import EmailMessage, EmailContact
from infra.web.schema import Email

fake = Faker()


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_email(self, from_: str, to: List[str], body: str, info: Info) -> Email:
        pubsub: MessageProvider = info.context.get('email_pubsub')

        # from_ = fake.email()
        # to = [fake.email() for e in range(random.randint(1, 4))]
        # body = fake.text()

        ent = EmailEntity(from_=from_, to=to, body=body)
        email = EmailMessage.create(from_=from_, to=', '.join(to), body=body)
        # for e in range(10):
        #     EmailContact.create(
        #         message=email,
        #         first_name=fake.first_name(),
        #         last_name=fake.last_name(),
        #         email=fake.email(),
        #     )

        await pubsub.publish(ent)

        return ent
