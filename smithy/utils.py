# coding=utf-8
from discord import Message
from discord.ext.commands import Bot

from smithy.database import manager, DBServer

__author__ = "Gareth Coles"
DEFAULT_PREFIX = "!"


async def get_prefix(bot: Bot, message: Message):
    server = await manager.get(DBServer, server_id=message.guild.id)  #: DBServer

    prefix = [bot.user.mention]

    if server:
        prefix.append(server.command_prefix)
    else:
        prefix.append(DEFAULT_PREFIX)

    return prefix
