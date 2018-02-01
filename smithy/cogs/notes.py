# coding=utf-8
from discord import TextChannel
from discord.colour import Colour
from discord.ext.commands import AutoShardedBot, Context, group

from smithy import database

__author__ = "Gareth Coles"

OPEN_COLOR = Colour.blurple()
CLOSED_COLOUR = Colour.red()
RESOLVED_COLOUR = Colour.green()


class Notes:
    """
    In-channel notes
    """

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @group(invoke_without_command=True)
    async def notes(self, ctx: Context):
        """
        In-channel notes management
        """

        await ctx.invoke(self.bot.get_command("help"), "notes")

    @notes.command()
    async def setup(self, ctx: Context, channel: TextChannel):
        """
        Set up the notes channel
        """

        pass

    @notes.command()
    async def clean(self, ctx: Context):
        """
        Empty the notes channel of non-note messages
        """

        # TODO: channel.purge()

        pass

    @notes.command()
    async def create(self, ctx: Context, *, text: str):
        """
        Create a new note
        """

        pass

    @notes.command()
    async def edit(self, ctx: Context, id: int, *, text: str):
        """
        Edit an existing note
        """

        pass

    @notes.command()
    async def close(self, ctx: Context, id: int):
        """
        Mark a note as "Closed"
        """

        pass

    @notes.command()
    async def resolve(self, ctx: Context, id: int):
        """
        Mark a note as "Resolved"
        """

        pass

    @notes.command()
    async def reopen(self, ctx: Context, id: int):
        """
        Mark a closed or resolved note as "Open"
        """

        pass


def setup(bot):
    bot.add_cog(Notes(bot))
    print("Cog loaded: Notes")
