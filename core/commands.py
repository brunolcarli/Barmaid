import discord
from discord.ext import commands

from barmaid.settings.common import (MAIN_CHANNEL, __version__, COIN_INCREASE_VALUE)
from core.models import User


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


@client.event
async def on_message(message):
    if message.author.bot:
        return

    await client.process_commands(message)

    server = message.guild.id
    author = message.author.id
    discord_id = f'{server}:{author}'

    user = User(discord_id)
    user.add_coin(COIN_INCREASE_VALUE)
    print(f'User {discord_id} earned {COIN_INCREASE_VALUE} coins!')


@client.command()
async def version(ctx):
    """
    Pings the bot to return its current version.
    """
    await ctx.send(f'Running version: {__version__}')


@client.command(aliases=['fds', 'coins', 'wallet'])
async def funds(ctx):
    """
    Checks your current coin amount.
    """
    server = ctx.guild.id
    author = ctx.author.id

    discord_id = f'{server}:{author}'
    user = User(discord_id)
    coins = int(user.coins)

    label = 'coin' if coins == 1 else 'coins'

    embed = discord.Embed(color=0x1E1E1E, type='rich')
    embed.add_field(name='Name:', value=ctx.author.name, inline=False)
    embed.add_field(
        name='Your balance:',
        value=f':coin: : {coins} {label}',
        inline=True
    )
    avatar = f'{ctx.author.avatar_url.BASE}{ctx.author.avatar_url._url}'
    embed.set_thumbnail(url=avatar)

    await ctx.send('Funds', embed=embed)