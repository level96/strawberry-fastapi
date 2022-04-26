from typing import List

import strawberry

from faker import Faker
from strawberry.subscriptions import GRAPHQL_TRANSPORT_WS_PROTOCOL, GRAPHQL_WS_PROTOCOL
from strawberry.fastapi import GraphQLRouter
from strawberry.extensions import QueryDepthLimiter
from fastapi import FastAPI

from infra.messaging.provider import MessageProvider
from infra.storage.repository import EmailInMemRepo
from infra.web.mutations import Mutation
from infra.web.queries import Query
from infra.web.schema import EmailContact
from infra.web.subscriptions import Subscription

from strawberry.dataloader import DataLoader
from infra.storage.models import (
    EmailMessage as EmailMessageModel,
    EmailContact as EmailContactModel,
)

EMAIL_CHANNEL = 'email'
SMS_CHANNEL = 'sms'

fake = Faker()

INMEM_REPO = EmailInMemRepo()


async def load_email_contacts(keys) -> List[EmailContact]:
    res = [c for c in EmailContactModel.select().filter(EmailContactModel.id << keys)]
    return res


async def load_emails(keys) -> List[EmailMessageModel]:
    res = [c for c in EmailMessageModel.select().filter(EmailMessageModel.id << keys)]
    return res


async def load_contact_ids_by_email(keys) -> List:
    res = {}
    qs = EmailContactModel.select(EmailMessageModel.id, EmailContactModel.id)
    qs = qs.join(EmailMessageModel)
    qs = qs.filter(EmailMessageModel.id << keys)
    for c in qs:
        if c.message_id not in res:
            res[c.message_id] = [c.id]
        else:
            res[c.message_id].append(c.id)

    return res.items()


async def get_context():
    return {
        "repo": INMEM_REPO,
        'email_pubsub': MessageProvider(channel=EMAIL_CHANNEL),
        'sms_pubsub': MessageProvider(channel=SMS_CHANNEL),
        'emails_loader': DataLoader(load_fn=load_emails),
        'contacts_loader': DataLoader(load_fn=load_email_contacts),
        'contact_ids_by_email_loader': DataLoader(load_fn=load_contact_ids_by_email)
    }


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    # extensions=[QueryDepthLimiter(max_depth=3)]
)
graphql_app = GraphQLRouter(
    schema,
    subscription_protocols=[GRAPHQL_TRANSPORT_WS_PROTOCOL, GRAPHQL_WS_PROTOCOL],
    context_getter=get_context
)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
