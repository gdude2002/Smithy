# coding=utf-8
from discord import TextChannel
from discord.colour import Colour
from discord.ext.commands import AutoShardedBot, Context, group, guild_only, has_permissions
from peewee import DoesNotExist

from smithy.database import manager, DBServer

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
    @guild_only()
    @has_permissions(manage_channels=True)
    async def setup(self, ctx: Context, *, channel: TextChannel):
        """
        Set up the notes channel

        This doesn't have to be an empty channel (notes will be appended to it), but if you decide you
        want to have a dedicated channel, please note that the "notes clean" command will completely wipe the channel.
        """

        try:
            server = await manager.get(DBServer, server_id=ctx.guild.id)
        except DoesNotExist:
            await ctx.send("**Error**: Server not in database.\n\n*Sorry! Please let us know!*")
            return

        if channel in ctx.guild.channels:
            server.notes_channel = channel.id
            await manager.update(server, [DBServer.notes_channel])
            await ctx.send(
                f"**Success**: Notes channel set to {channel.name} ({channel.id})\n\n"
                f"Please remember that the `notes clean` command will completely wipe this channel's messages and "
                f"replace them with your collection of notes."
            )
        else:
            await ctx.send(f"Bad argument: Channel \"{channel.id}\" not found.")
            await ctx.invoke(self.bot.get_command("help"), "notes", "setup")

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
