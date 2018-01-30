# coding=utf-8
from discord import Message
from discord.ext.commands import Bot

__author__ = "Gareth Coles"


class Logging:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def on_ready(self):
        print("Ready!")

    async def on_message(self, message: Message):
        if not message.guild:  # It's a DM
            print(
                f"@{self.bot.user.name}#{self.bot.user.discriminator} | "
                f"@{message.author.name}#{message.author.discriminator} -> "
                f"{message.clean_content}"
            )
        else:
            print(
                f"{message.guild.name} | #{message.channel.name} | "
                f"@{message.author.name}#{message.author.discriminator} -> "
                f"{message.clean_content}"
            )


def setup(bot):
    bot.add_cog(Logging(bot))
    print("Cog loaded: Logging")
