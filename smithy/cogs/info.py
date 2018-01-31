# coding=utf-8
from discord.ext.commands import Bot

__author__ = "Gareth Coles"


class Info:
    """
    Info channel management commands
    """

    def __init__(self, bot: Bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Info(bot))
    print("Cog loaded: Info")
