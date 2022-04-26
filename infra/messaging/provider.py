import json
import aioredis

from typing import AsyncGenerator
from dataclasses import asdict
from core.entities import BaseEntity


class MessageProvider:
    channel: str = ''
    url: str = 'redis://localhost'

    def __init__(self, channel: str):
        self.channel = channel
        self.server = aioredis.from_url(self.url)
        self.pubsub = self.server.pubsub()

    async def publish(self, data: BaseEntity):
        await self.server.publish(self.channel, json.dumps(asdict(data), default=str))

    async def messages(self) -> AsyncGenerator:
        await self.pubsub.subscribe(self.channel)

        while True:
            message = await self.pubsub.get_message()
            if message and message['type'] == 'message':
                yield json.loads(message['data'])

    async def get_message(self) -> BaseEntity:
        message = await self.pubsub.get_message(
            ignore_subscribe_messages=True,
            timeout=60,
        )
        return message
