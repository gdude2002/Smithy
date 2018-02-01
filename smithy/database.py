# coding=utf-8
import peewee
# peewee-db-evolve patches the database instances on import for some reason
import peeweedbevolve  # flake8: noqua

from peewee_async import Manager
from peewee_asyncext import PooledPostgresqlExtDatabase
from playhouse.fields import ManyToManyField
from playhouse.postgres_ext import BinaryJSONField

from smithy.config import DATABASE
from smithy.constants import NOTE_OPEN, NOTE_CLOSED, NOTE_RESOLVED

__author__ = "Gareth Coles"
database = PooledPostgresqlExtDatabase(**DATABASE, register_hstore=False)
manager = Manager(database)


class Module(peewee.Model):
    name = peewee.CharField(unique=True)

    class Meta:
        database = database


class DBServer(peewee.Model):
    server_id = peewee.IntegerField(unique=True)
    bot_present = peewee.BooleanField(default=False)
    command_prefix = peewee.CharField(default="!")
    modules = ManyToManyField(Module, related_name="servers")
    info_channel = peewee.IntegerField(null=True)
    notes_channel = peewee.IntegerField(null=True)

    class Meta:
        database = database


class InfoSectionType(peewee.Model):
    name = peewee.CharField(unique=True)

    class Meta:
        database = database


class InfoSection(peewee.Model):
    server = peewee.ForeignKeyField(DBServer, related_name="sections")
    name = peewee.CharField(max_length=512)
    header = peewee.CharField(max_length=2000)
    footer = peewee.CharField(max_length=2000)
    type = ManyToManyField(InfoSectionType)
    data = BinaryJSONField()

    class Meta:
        database = database


class Note(peewee.Model):
    server = peewee.ForeignKeyField(DBServer, related_name="notes")
    message_id = peewee.IntegerField()
    status = peewee.IntegerField(default=NOTE_OPEN)
    text = peewee.CharField(max_length=1000)
    date = peewee.DateTimeField()
    submitter_name = peewee.CharField()
    submitter_id = peewee.IntegerField()

    @property
    def open(self):
        return self.status == NOTE_OPEN

    @property
    def closed(self):
        return self.status == NOTE_CLOSED

    @property
    def resolved(self):
        return self.status == NOTE_RESOLVED

    class Meta:
        database = database


def evolve(interactive=True) -> None:
    database.evolve(interactive=interactive)  # flake8: noqa


async def ensure_modules(*modules) -> None:
    for db_module in await manager.get(Module):
        if db_module.name not in modules:
            manager.delete(db_module)

    for module in modules:
        manager.get_or_create(Module, name=module)


async def ensure_sections(*sections) -> None:
    for db_section in await manager.get(InfoSectionType):
        if db_section.name not in sections:
            manager.delete(db_section)

    for section in sections:
        manager.get_or_create(InfoSectionType, name=section)
