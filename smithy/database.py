# coding=utf-8
import datetime
from asyncio import get_event_loop

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


MODULES = [
    "bot", "events", "info", "notes", "relay"
]

SECTIONS = [
    "bullet_list", "faq", "numbered_list", "text", "url"
]


class Module(peewee.Model):
    name = peewee.CharField(unique=True)

    class Meta:
        database = database


class DBServer(peewee.Model):
    server_id = peewee.BigIntegerField(unique=True)
    bot_present = peewee.BooleanField(default=False)
    command_prefix = peewee.CharField(default="!")
    # modules = ManyToManyField(Module, related_name="servers")
    info_channel = peewee.BigIntegerField(null=True)
    notes_channel = peewee.BigIntegerField(null=True)

    async def has_module(self, module_name: str) -> bool:
        modules = await manager.execute(
            Module.select()
            .join(DBServerModuleThrough)
            .join(DBServer)
            .where(DBServer.id == self.id)
            .where(Module.name == module_name)
        )

        return bool(modules)

    async def add_module(self, module_name: str):
        module = await manager.get(Module, name=module_name)

        if not module:
            return

        await manager.create(
            DBServerModuleThrough, server_id=self.id, module_id=module.id
        )

    async def remove_module(self, module_name: str):
        module = await manager.execute(
            Module.select()
            .join(DBServerModuleThrough)
            .join(DBServer)
            .where(DBServer.id == self.id)
            .where(Module.name == module_name)
        )

        if not module:
            return

        await manager.delete(
            await manager.get(DBServerModuleThrough, server_id=self.id, module_id=module[0].id)
        )

    class Meta:
        database = database


class DBServerModuleThrough(peewee.Model):
    server = peewee.ForeignKeyField(DBServer)
    module = peewee.ForeignKeyField(Module)

    class Meta:
        database = database


class InfoSection(peewee.Model):
    server = peewee.ForeignKeyField(DBServer, related_name="sections")
    name = peewee.CharField(max_length=512)
    header = peewee.CharField(max_length=2000)
    footer = peewee.CharField(max_length=2000)
    type = peewee.CharField(max_length=30)
    data = BinaryJSONField()

    class Meta:
        database = database


class Note(peewee.Model):
    server = peewee.ForeignKeyField(DBServer, related_name="notes")
    message_id = peewee.BigIntegerField()
    status = peewee.IntegerField(default=NOTE_OPEN)
    text = peewee.CharField(max_length=1000)
    date = peewee.DateTimeField(default=datetime.datetime.now)
    submitter_name = peewee.CharField()
    submitter_id = peewee.BigIntegerField()
    note_id = peewee.BigIntegerField()

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

    loop = get_event_loop()
    loop.run_until_complete(ensure_modules(*MODULES))
    print(f"Ensured module list: {', '.join(MODULES)}")


async def ensure_modules(*modules) -> None:
    for db_module in await manager.execute(Module.select()):
        if db_module.name not in modules:
            await manager.delete(db_module)

    for module in modules:
        await manager.get_or_create(Module, name=module)


def disable_sync():
    database.allow_sync = False
