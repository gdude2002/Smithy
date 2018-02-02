# coding=utf-8
from discord import Guild
from discord.ext.commands import AutoShardedBot
from peewee import DoesNotExist

from smithy.database import manager, DBServer

__author__ = "Gareth Coles"


class Events:
    """
    No commands, just event handlers
    """

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    async def on_guild_join(self, guild: Guild):
        try:
            await manager.get(DBServer, server_id=guild.id)
        except DoesNotExist:
            print(f"Adding guild to DB: {guild.name} ({guild.id})")

            await manager.create(
                DBServer, server_id=guild.id, bot_present=True
            )

    async def on_ready(self):
        print("Checking guilds...")
        for guild in self.bot.guilds:
            if self.bot.shard_id is None or self.bot.shard_id == guild.shard_id:
                await self.on_guild_join(guild)


def setup(bot):
    bot.add_cog(Events(bot))
    print("Cog loaded: Events")
