import json
from typing import AsyncGenerator

import strawberry
from strawberry.types import Info

from infra.messaging.provider import MessageProvider
from infra.web.schema import Email, Message


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def email(self, info: Info) -> AsyncGenerator[Email, None]:
        pubsub: MessageProvider = info.context.get('email_pubsub')

        async for msg in pubsub.messages():
            yield Email.from_dict(msg)

    @strawberry.subscription
    async def sms(self, info: Info) -> AsyncGenerator[Message, None]:
        pubsub: MessageProvider = info.context.get('sms_pubsub')

        async for msg in pubsub.messages():
            yield Message.from_dict(msg)
