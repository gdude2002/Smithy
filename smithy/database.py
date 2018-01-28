# coding=utf-8
import asyncio

import peewee

from peewee_async import Manager
from peewee_asyncext import PooledPostgresqlExtDatabase
from playhouse.postgres_ext import ArrayField
from psycopg2._psycopg import AsIs
from psycopg2.extensions import register_adapter

from smithy.config import DATABASE

__author__ = "Gareth Coles"
database = PooledPostgresqlExtDatabase(**DATABASE, register_hstore=False)
manager = Manager(database)


class Module(peewee.Model):
    name = peewee.CharField()

    class Meta:
        database = database


class DBServer(peewee.Model):
    server_id = peewee.IntegerField()
    bot_present = peewee.BooleanField(default=False)
    command_prefix = peewee.CharField(default="!")
    modules = ArrayField(lambda: peewee.ForeignKeyField(Module, to_field=Module.id))
    info_channel = peewee.IntegerField(null=True)
    notes_channel = peewee.IntegerField(null=True)

    class Meta:
        database = database


def create_tables() -> None:
    DBServer.create_table(fail_silently=True)
    Module.create_table(fail_silently=True)


def adapt_model(model):
    return AsIs("%s" % model.id)


register_adapter(Module, adapt_model)


if __name__ == "__main__":
    async def test():
        create_tables()
        module = await manager.create_or_get(Module, id=1, name="test")
        server = await manager.create_or_get(DBServer, server_id=0, modules=[module])
        print(server)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
