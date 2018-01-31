# coding=utf-8
from discord.ext.commands import Bot, Context, group

from smithy import database

__author__ = "Gareth Coles"


class Notes:
    """
    In-channel notes
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @group(invoke_without_command=True)
    async def notes(self, ctx: Context):
        """
        In-channel notes management
        """

        pass  # TODO: Error message

    @notes.command()
    async def setup(self, ctx: Context):
        """
        Set up the notes channel
        """

        pass

    @notes.command()
    async def clean(self, ctx: Context):
        """
        Empty the notes channel of non-note messages
        """

        pass

    @notes.command()
    async def create(self, ctx: Context):
        """
        Create a new note
        """

        pass

    @notes.command()
    async def edit(self, ctx: Context):
        """
        Edit an existing note
        """

        pass

    @notes.command()
    async def close(self, ctx: Context):
        """
        Mark a note as "Closed"
        """

        pass

    @notes.command()
    async def resolve(self, ctx: Context):
        """
        Mark a note as "Resolved"
        """

        pass

    @notes.command()
    async def reopen(self, ctx: Context):
        """
        Mark a closed or resolved note as "Open"
        """

        pass


def setup(bot):
    bot.add_cog(Notes(bot))
    print("Cog loaded: Notes")
