import discord
from discord.ext import commands

from barmaid.settings.common import (MAIN_CHANNEL, __version__)



client = commands.Bot(command_prefix='>')


@client.event
async def on_member_join(member):
    """
    Sends a welcome message on the main channel when a new member enters
    the guild (server).
    ~~At least it is supposed to send a welcome message~~
    """
    text = 'Welcome'

    channel = client.get_channel(MAIN_CHANNEL)
    if channel:
        return await channel.send(text)


@client.event
async def on_ready():
    """
    Prints a "log message" on the shell informing the bot (system)  was
    initialized and running.
    """
    print("System loaded and running!")


@client.command()
async def version(ctx):
    """
    Pings the bot to return its current version.
    """
    await ctx.send(f'Running version: {__version__}')
