# coding=utf-8
from discord.ext.commands import AutoShardedBot

__author__ = "Gareth Coles"


class Relay:
    """
    Cross-channel message relaying
    """

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Relay(bot))
    print("Cog loaded: Relay")
