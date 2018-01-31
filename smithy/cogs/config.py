# coding=utf-8
from discord.ext.commands import Bot

__author__ = "Gareth Coles"


class Config:
    """
    Configuration commands
    """

    def __init__(self, bot: Bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Config(bot))
    print("Cog loaded: Config")
