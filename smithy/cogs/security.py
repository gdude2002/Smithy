# coding=utf-8
from discord.ext.commands import Bot, Context

__author__ = "Gareth Coles"


class Security:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.check(self.check_not_bot)

    async def check_not_bot(self, ctx: Context):
        return not ctx.author.bot


def setup(bot):
    bot.add_cog(Security(bot))
    print("Cog loaded: Security")
