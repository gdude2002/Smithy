# coding=utf-8
from discord.ext.commands import AutoShardedBot

__author__ = "Gareth Coles"


class Events:
    """
    No commands, just event handlers
    """

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Events(bot))
    print("Cog loaded: events")
