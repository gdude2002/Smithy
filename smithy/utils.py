# coding=utf-8
from discord import Message
from discord.ext.commands import Bot, when_mentioned_or
from peewee import DoesNotExist

from smithy.database import manager, DBServer

__author__ = "Gareth Coles"
DEFAULT_PREFIX = "!"


async def get_prefix(bot: Bot, message: Message):
    if not message.guild:
        return when_mentioned_or(DEFAULT_PREFIX)(bot, message)
    try:
        server = await manager.get(DBServer, server_id=message.guild.id)  #: DBServer
        return when_mentioned_or(server.command_prefix)
    except DoesNotExist:
        return when_mentioned_or(DEFAULT_PREFIX)(bot, message)
