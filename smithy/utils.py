# coding=utf-8
from discord import Message, TextChannel
from discord.ext.commands import AutoShardedBot, when_mentioned_or
from peewee import DoesNotExist

from smithy.database import manager, DBServer

__author__ = "Gareth Coles"
DEFAULT_PREFIX = "!"


async def get_prefix(bot: AutoShardedBot, message: Message):
    if not message.guild:
        return when_mentioned_or(DEFAULT_PREFIX)(bot, message)
    try:
        server = await manager.get(DBServer, server_id=message.guild.id)  #: DBServer
        return when_mentioned_or(server.command_prefix)(bot, message)
    except DoesNotExist:
        return when_mentioned_or(DEFAULT_PREFIX)(bot, message)
