# coding=utf-8
import argparse

from discord.ext.commands import Bot

from smithy.database import evolve as db_evolve
from smithy.config import TOKEN
from smithy.utils import get_prefix

__author__ = "Gareth Coles"


def run():
    bot = Bot(command_prefix=get_prefix)
    bot.owner_id = 109040264529608704

    # Internal stuff
    bot.load_extension("smithy.cogs.logging")
    bot.load_extension("smithy.cogs.security")
    bot.load_extension("smithy.cogs.events")

    # Owner/debug
    bot.load_extension("smithy.cogs.eval")

    # User stuff
    bot.load_extension("smithy.cogs.config")
    bot.load_extension("smithy.cogs.info")
    bot.load_extension("smithy.cogs.relay")

    bot.run(TOKEN)


def evolve():
    db_evolve()


parser = argparse.ArgumentParser(prog="smithy")
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--run", help="Run the bot", action="store_true")
group.add_argument("--evolve", help="Update the database schema - evolve the DB", action="store_true")

args = parser.parse_args()

if args.run:
    run()
elif args.evolve:
    evolve()
else:
    parser.print_usage()
