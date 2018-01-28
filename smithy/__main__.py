# coding=utf-8
from discord.ext.commands import Bot

__author__ = "Gareth Coles"

bot = Bot(command_prefix="!")
bot.owner_id = 109040264529608704

bot.load_extension("smithy.cogs.logging")
bot.load_extension("smithy.cogs.security")
bot.load_extension("smithy.cogs.eval")

bot.run("")
