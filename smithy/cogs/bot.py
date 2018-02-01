# coding=utf-8
from discord import Embed
from discord.ext.commands import AutoShardedBot, group, Context

__author__ = "Gareth Coles"


class Bot:
    """
    Bot information commands
    """

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @group(invoke_without_command=True, name="bot")
    async def bot_group(self, ctx: Context):
        """
        Bot information commands
        """

        await ctx.invoke(self.bot.get_command("help"), "bot")

    @bot_group.command()
    async def info(self, ctx: Context):
        """
        Get information about the current bot
        """

        if self.bot.shard_id is None:
            embed = Embed(
                description="Smithy is a general-purpose bot, built with some unusual features.\n\n"
                            "**Smithy is currently not sharded.**",
                url="https://github.com/gdude2002/Smithy"
            )
        else:
            embed = Embed(
                description="Smithy is a general-purpose bot, built with some unusual features.",
                url="https://github.com/gdude2002/Smithy"
            )
            embed.add_field(
                name="Total Shards", value=self.bot.shard_count
            )
            embed.add_field(
                name="Current Shard", value=self.bot.shard_id
            )

        embed.add_field(name="Visible Guilds", value=str(len(self.bot.guilds)))
        embed.add_field(name="Visible Users", value=str(len(self.bot.users)))

        embed.set_author(
            name="Smithy",
            url="https://github.com/gdude2002/Smithy",
            icon_url="https://dl.dropboxusercontent.com/s/44524s0sexz3tvl/anvil256.png"
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Bot(bot))
    print("Cog loaded: Bot")
