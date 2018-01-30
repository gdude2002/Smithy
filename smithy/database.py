# coding=utf-8
import peewee
# peewee-db-evolve patches the database instances on import for some reason
import peeweedbevolve  # flake8: noqua

from peewee_async import Manager
from peewee_asyncext import PooledPostgresqlExtDatabase
from playhouse.fields import ManyToManyField

from smithy.config import DATABASE

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


def evolve() -> None:
    database.evolve(  # flake8: noqa
        [
            DBServer,
            DBServer.modules.get_through_model(),
            Module,
        ]
    )
