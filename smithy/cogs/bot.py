# coding=utf-8
from discord.ext.commands import Bot as DBot

__author__ = "Gareth Coles"


class Bot:
    """
    Bot information commands
    """

    def __init__(self, bot: DBot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Bot(bot))
    print("Cog loaded: Bot")
