import asyncio

from faker import Faker

from core.entities import Email, Message
from infra.messaging.provider import MessageProvider

EMAIL_CHANNEL = 'email'
SMS_CHANNEL = 'sms'


async def main():
    fake = Faker()

    email_message_provider = MessageProvider(channel=EMAIL_CHANNEL)
    sms_message_provider = MessageProvider(channel=SMS_CHANNEL)

    while True:
        mail = Email(from_=fake.email(), to=[fake.email()], body=fake.text()[:255])
        sms = Message(from_=fake.msisdn(), to=[fake.msisdn()], body=fake.text()[:100])

        await email_message_provider.publish(mail)
        await sms_message_provider.publish(sms)

        await asyncio.sleep(1)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exited")
