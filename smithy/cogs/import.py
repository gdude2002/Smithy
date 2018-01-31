# coding=utf-8
from discord.ext.commands import Bot

__author__ = "Gareth Coles"


class Import:
    """
    Import old InfoBot and RelayBot data
    """

    def __init__(self, bot: Bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Import(bot))
    print("Cog loaded: Import")
