# coding=utf-8
import asyncio

import peeweedbevolve
import peewee

from peewee_async import Manager
from peewee_asyncext import PooledPostgresqlExtDatabase
from playhouse.fields import ManyToManyField

from smithy.config import DATABASE

__author__ = "Gareth Coles"
database = PooledPostgresqlExtDatabase(**DATABASE, register_hstore=False)
manager = Manager(database)


class Module(peewee.Model):
    name = peewee.CharField()

    class Meta:
        database = database


class DBServer(peewee.Model):
    server_id = peewee.IntegerField(unique=True)
    bot_present = peewee.BooleanField(default=False)
    command_prefix = peewee.CharField(default="!")
    modules = ManyToManyField(Module, related_name="users")
    info_channel = peewee.IntegerField(null=True)
    notes_channel = peewee.IntegerField(null=True)

    class Meta:
        database = database


def evolve() -> None:
    database.evolve(
        [
            DBServer,
            DBServer.modules.get_through_model(),
            Module,
        ]
    )
