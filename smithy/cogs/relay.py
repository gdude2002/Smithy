# coding=utf-8
from discord.ext.commands import Bot

__author__ = "Gareth Coles"


class Relay:
    def __init__(self, bot: Bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Relay(bot))
    print("Cog loaded: Relay")
