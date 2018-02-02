# coding=utf-8
import datetime
from discord import TextChannel, Guild, Embed, HTTPException, Member
from discord.colour import Colour
from discord.ext.commands import AutoShardedBot, Context, group, guild_only, has_permissions
from peewee import DoesNotExist

from smithy.constants import NOTE_CLOSED, NOTE_OPEN, NOTE_RESOLVED
from smithy.database import manager, DBServer, Note

__author__ = "Gareth Coles"

CLOSED_COLOUR = Colour.red()
OPEN_COLOR = Colour.blurple()
RESOLVED_COLOUR = Colour.green()


class Notes:
    """
    In-channel notes
    """

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @group(invoke_without_command=True, aliases=["note"])
    async def notes(self, ctx: Context):
        """
        In-channel notes management
        """

        await ctx.invoke(self.bot.get_command("help"), "notes")

    @notes.command(aliases=["set-channel"])
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

            await manager.update(server, (DBServer.notes_channel,))
            await ctx.send(
                f"**Success**: Notes channel set to {channel.name} ({channel.id})\n\n"
                f"Please remember that the `notes clean` command will completely wipe this channel's messages and "
                f"replace them with your collection of notes."
            )
        else:
            await ctx.send(f"Bad argument: Channel \"{channel.id}\" not found.")
            await ctx.invoke(self.bot.get_command("help"), "notes", "setup")

    @notes.command(aliases=["clear", "purge"])
    @guild_only()
    @has_permissions(manage_channels=True)
    async def clean(self, ctx: Context):
        """
        Empty the notes channel of non-note messages
        """

        try:
            server = await manager.get(DBServer, server_id=ctx.guild.id)
        except DoesNotExist:
            await ctx.send("**Error**: Server not in database\n\n*Sorry! Please let us know!*")
            return

        if not server.notes_channel:
            await ctx.send("**Error**: No notes channel has been set - please use the `notes setup` command to set one")

        channel = self.bot.get_channel(server.notes_channel)

        if not channel:
            await ctx.send("**Error**: The configured channel appears to not exist. Please set a new one!")
            return

        status_message = await ctx.send("Please wait, clearing channel...")

        await channel.purge(bulk=True, limit=None)

        try:
            await status_message.edit(content="Please wait, re-posting notes...")
        except HTTPException:  # Might've just deleted it
            status_message = await ctx.send("Please wait, re-posting notes...")

        await self.send_all_notes(ctx.guild, server)

        try:
            await status_message.edit(content="Notes channel cleaned.", delete_after=10)
        except HTTPException:  # Might've just deleted it
            await ctx.send("Notes channel cleaned.", delete_after=10)

    @notes.command(aliases=["add"])
    @guild_only()
    async def create(self, ctx: Context, *, text: str):
        """
        Create a new note
        """

        try:
            server = await manager.get(DBServer, server_id=ctx.guild.id)
        except DoesNotExist:
            await ctx.send("**Error**: Server not in database\n\n*Sorry! Please let us know!*")
            return

        if not server.notes_channel:
            await ctx.send("**Error**: No notes channel has been set - please use the `notes setup` command to set one")

        channel = self.bot.get_channel(server.notes_channel)

        if not channel:
            await ctx.send("**Error**: The configured channel appears to not exist. Please set a new one!")
            return

        note_id = await manager.count(Note.select().where(Note.server == server)) + 1

        embed = Embed(
            title=f"Note: {note_id} (Open)",
            description=text
        )

        embed.colour = OPEN_COLOR
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.timestamp = datetime.datetime.now()

        message = await channel.send(embed=embed)

        await manager.create(
            Note,
            server=server, message_id=message.id, text=text, submitter_name=ctx.author.name,
            submitter_id=ctx.author.id, note_id=note_id
        )

        await ctx.send("Note created.", delete_after=10)

    @notes.command()
    @guild_only()
    async def edit(self, ctx: Context, note_id: int, *, text: str):
        """
        Edit an existing note
        """

        try:
            server = await manager.get(DBServer, server_id=ctx.guild.id)
        except DoesNotExist:
            await ctx.send("**Error**: Server not in database\n\n*Sorry! Please let us know!*")
            return

        if not server.notes_channel:
            await ctx.send("**Error**: No notes channel has been set - please use the `notes setup` command to set one")

        channel = self.bot.get_channel(server.notes_channel)

        if not channel:
            await ctx.send("**Error**: The configured channel appears to not exist. Please set a new one!")
            return

        try:
            note = await manager.get(Note, server=server, note_id=note_id)
        except DoesNotExist:
            await ctx.send("**Error**: Can't find that note, make sure the note ID is correct!")
            return

        if note.submitter_id != ctx.author.id and not channel.permissions_for(ctx.author).manage_messages:
            await ctx.send("**Error**: You don't have permission to edit other people's notes!")
            return

        note.text = text
        await manager.update(note, (Note.text,))

        message = await channel.get_message(note.message_id)
        embed = message.embeds[0]
        embed.description = text

        await message.edit(embed=embed)
        await ctx.send("Note updated.", delete_after=10)

    @notes.command(aliases=["closed"])
    @guild_only()
    async def close(self, ctx: Context, note_id: int):
        """
        Mark a note as "Closed"
        """

        try:
            server = await manager.get(DBServer, server_id=ctx.guild.id)
        except DoesNotExist:
            await ctx.send("**Error**: Server not in database\n\n*Sorry! Please let us know!*")
            return

        if not server.notes_channel:
            await ctx.send("**Error**: No notes channel has been set - please use the `notes setup` command to set one")

        channel = self.bot.get_channel(server.notes_channel)

        if not channel:
            await ctx.send("**Error**: The configured channel appears to not exist. Please set a new one!")
            return

        try:
            note = await manager.get(Note, server=server, note_id=note_id)
        except DoesNotExist:
            await ctx.send("**Error**: Can't find that note, make sure the note ID is correct!")
            return

        if note.submitter_id != ctx.author.id and not channel.permissions_for(ctx.author).manage_messages:
            await ctx.send("**Error**: You don't have permission to edit other people's notes!")
            return

        if note.status == NOTE_CLOSED:
            await ctx.send("**Error**: That note is already marked as closed")
            return

        note.status = NOTE_CLOSED
        await manager.update(note, (Note.status,))

        message = await channel.get_message(note.message_id)
        embed = message.embeds[0]
        embed.title = f"Note: {note_id} (Closed)"
        embed.colour = CLOSED_COLOUR

        await message.edit(embed=embed)
        await ctx.send("Note updated.", delete_after=10)

    @notes.command(aliases=["done", "finish", "finished", "resolved"])
    @guild_only()
    async def resolve(self, ctx: Context, note_id: int):
        """
        Mark a note as "Resolved"
        """

        try:
            server = await manager.get(DBServer, server_id=ctx.guild.id)
        except DoesNotExist:
            await ctx.send("**Error**: Server not in database\n\n*Sorry! Please let us know!*")
            return

        if not server.notes_channel:
            await ctx.send("**Error**: No notes channel has been set - please use the `notes setup` command to set one")

        channel = self.bot.get_channel(server.notes_channel)

        if not channel:
            await ctx.send("**Error**: The configured channel appears to not exist. Please set a new one!")
            return

        try:
            note = await manager.get(Note, server=server, note_id=note_id)
        except DoesNotExist:
            await ctx.send("**Error**: Can't find that note, make sure the note ID is correct!")
            return

        if note.submitter_id != ctx.author.id and not channel.permissions_for(ctx.author).manage_messages:
            await ctx.send("**Error**: You don't have permission to edit other people's notes!")
            return

        if note.status == NOTE_RESOLVED:
            await ctx.send("**Error**: That note is already marked as resolved")
            return

        note.status = NOTE_RESOLVED
        await manager.update(note, (Note.status,))

        message = await channel.get_message(note.message_id)
        embed = message.embeds[0]
        embed.title = f"Note: {note_id} (Resolved)"
        embed.color = RESOLVED_COLOUR

        await message.edit(embed=embed)
        await ctx.send("Note updated.", delete_after=10)

    @notes.command(aliases=["open", "opened", "reopened"])
    @guild_only()
    async def reopen(self, ctx: Context, note_id: int):
        """
        Mark a closed or resolved note as "Open"
        """

        try:
            server = await manager.get(DBServer, server_id=ctx.guild.id)
        except DoesNotExist:
            await ctx.send("**Error**: Server not in database\n\n*Sorry! Please let us know!*")
            return

        if not server.notes_channel:
            await ctx.send("**Error**: No notes channel has been set - please use the `notes setup` command to set one")

        channel = self.bot.get_channel(server.notes_channel)

        if not channel:
            await ctx.send("**Error**: The configured channel appears to not exist. Please set a new one!")
            return

        try:
            note = await manager.get(Note, server=server, note_id=note_id)
        except DoesNotExist:
            await ctx.send("**Error**: Can't find that note, make sure the note ID is correct!")
            return

        if note.submitter_id != ctx.author.id and not channel.permissions_for(ctx.author).manage_messages:
            await ctx.send("**Error**: You don't have permission to edit other people's notes!")
            return

        if note.status == NOTE_OPEN:
            await ctx.send("**Error**: That note is already marked as open")
            return

        note.status = NOTE_OPEN
        await manager.update(note, (Note.status,))

        message = await channel.get_message(note.message_id)
        embed = message.embeds[0]
        embed.title = f"Note: {note_id} (Open)"
        embed.color = OPEN_COLOR

        await message.edit(embed=embed)
        await ctx.send("Note updated.", delete_after=10)

    async def send_all_notes(self, guild: Guild, server: DBServer=None):
        if server is None:
            try:
                server = await manager.get(DBServer, server_id=guild.id)
            except DoesNotExist:
                return

        if not server.notes_channel:
            return

        channel = self.bot.get_channel(server.notes_channel)
        notes = await manager.execute(
            Note.select().where(Note.server_id == server.id).order_by(Note.note_id)
        )

        if not notes:
            return

        for note in notes:
            await self.send_note(channel, note)

    async def send_note(self, channel: TextChannel, note: Note):
        embed = Embed(
            description=note.text
        )

        if note.status == NOTE_CLOSED:
            embed.colour = CLOSED_COLOUR
            embed.title = f"Note: {note.note_id} (Closed)"
            embed.timestamp = note.date
        elif note.status == NOTE_OPEN:
            embed.colour = OPEN_COLOR
            embed.title = f"Note: {note.note_id} (Open)"
            embed.timestamp = note.date
        elif note.status == NOTE_RESOLVED:
            embed.colour = RESOLVED_COLOUR
            embed.title = f"Note: {note.note_id} (Resolved)"
            embed.timestamp = note.date

        user = self.bot.get_user(note.submitter_id)

        if user:
            embed.set_footer(text=user.name, icon_url=user.avatar_url)
        else:
            embed.set_footer(text=note.submitter_name)

        message = await channel.send(embed=embed)
        note.message_id = message.id
        await manager.update(note, (Note.message_id,))


def setup(bot):
    bot.add_cog(Notes(bot))
    print("Cog loaded: Notes")
