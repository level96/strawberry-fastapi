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
        await pubsub.subscribe()

        while True:
            message = await pubsub.get_message()
            if message and message['type'] == 'message':
                yield Email.from_dict(json.loads(message['data']))

    @strawberry.subscription
    async def sms(self, info: Info) -> AsyncGenerator[Message, None]:
        pubsub: MessageProvider = info.context.get('sms_pubsub')
        await pubsub.subscribe()

        while True:
            message = await pubsub.get_message()
            if message and message['type'] == 'message':
                yield Message.from_dict(json.loads(message['data']))
