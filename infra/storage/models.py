import uuid
import datetime

from peewee import (
    Model,
    UUIDField,
    DateTimeField,
    SqliteDatabase,
    CharField,
    ForeignKeyField
)

database = SqliteDatabase('./database.db')


class BaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database


class SMSMessage(BaseModel):
    from_ = CharField(max_length=255)
    to = CharField(max_length=255)
    body = CharField(max_length=255)


class EmailMessage(BaseModel):
    from_ = CharField(max_length=255)
    to = CharField(max_length=255)
    body = CharField(max_length=255)


class EmailContact(BaseModel):
    message = ForeignKeyField(EmailMessage, backref='contacts')
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    email = CharField(max_length=255)


class SMSContact(BaseModel):
    message = ForeignKeyField(SMSMessage, backref='contacts')
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    number = CharField(max_length=255)


def migrate():
    database.create_tables([SMSMessage, EmailMessage, EmailContact, SMSContact])
