import discord
from discord.ext import commands

from barmaid.settings.common import (MAIN_CHANNEL, __version__, COIN_INCREASE_VALUE)
from core.models import User, ItemList, SpecificItem
from core.util import get_discord_id


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
    discord_id = get_discord_id(ctx.guild.id, ctx.author.id)
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


@client.command(aliases=['store', 'list'])
async def items(ctx):
    """
    Lists items for sale.
    """
    item_list = ItemList()

    embed = discord.Embed(color=0x1E1E1E, type='rich')
    for item in item_list.items:
        label = f'Code: {item.code} - {item.name}'
        embed.add_field(name=label, value=f'cost: {item.value} :coin:', inline=True)

    await ctx.send('Available items:', embed=embed)


@client.command(aliases=['v', 'item', 'code'])
async def view(ctx, code=None):
    """
    View details for specifi item by code.
        Usage example:
            >view 5
    """
    if not code:
        return await ctx.send('You must specify a item code!')

    if not code.isdigit():
        return await ctx.send('Item code must be a number.')

    try:
        item = SpecificItem(code)
    except NameError as err:
        return await ctx.send(err.args[0])

    try:
        picture = discord.File(item.sprite)
    except FileNotFoundError:
        return await ctx.send('Item not available.')

    embed = discord.Embed(color=0x1E1E1E, type='rich')
    embed.add_field(name='Name:', value=item.name, inline=True)
    embed.add_field(name='Cost:', value=f':coin: : {item.value} coins', inline=True)
    embed.add_field(name='Description:', value=item.description, inline=False)
    embed.add_field(name='Times sold:', value=item.sell_count, inline=False)

    embed.set_thumbnail(url=f'attachment://{picture.filename}')

    await ctx.send(f'Item code: {item.code}', embed=embed, file=picture)


@client.command()
async def buy(ctx, code=None):
    """
    Buy a item (if possible) by item code.
        Usage example:
            >buy 1
    """
    if not code:
        return await ctx.send('You must specify a item code!')

    if not code.isdigit():
        return await ctx.send('Item code must be a number.')

    # resolve user
    discord_id = get_discord_id(ctx.guild.id, ctx.author.id)
    user = User(discord_id)

    # resolve item
    try:
        item = SpecificItem(code)
    except NameError as err:
        return await ctx.send(err.args[0])

    try:
        picture = discord.File(item.sprite)
    except FileNotFoundError:
        return await ctx.send('Item not available.')

    # handle transaction possibility
    if user.coins < item.value:
        return await ctx.send('You dont have enough funds.')

    user.add_purchase(item)
    item.sell()

    embed = discord.Embed(color=0x1E1E1E, type='rich')
    msg = f'{item.name} for {item.value} :coin: coins!'
    embed.add_field(name=f'{ctx.author.name} bought:', value=msg, inline=True)
    embed.set_thumbnail(url=f'attachment://{picture.filename}')

    await ctx.send(f'Purchased', embed=embed, file=picture)


@client.command(aliases=['pch', 'ps'])
async def purchases(ctx, param=None):
    """
    Lists purchased items.
    If no param is given, lists the user purchased items;
    If param [a, all] is given, lists all purchased items count.
        Usage example:
            >ps
            >ps a
            >ps all
    """
    if not param:  # returns user purchases list
        # resolve user
        discord_id = get_discord_id(ctx.guild.id, ctx.author.id)
        user = User(discord_id)
        purchases = user.get_purchases()

        if not purchases:
            return await ctx.send('User did not buy anything yet.')

        embed = discord.Embed(color=0x1E1E1E, type='rich')
        for name, count in purchases.items():
            embed.add_field(name=name, value=count, inline=False)

        # Calculate total coins spent by the user
        items = ItemList()
        total = []
        for name, count in purchases.items():
            total.append(items[name].value * count)

        embed.add_field(name='Total amount spent:', value=f'{sum(total)} :coin:', inline=False)

        avatar = f'{ctx.author.avatar_url.BASE}{ctx.author.avatar_url._url}'
        embed.set_thumbnail(url=avatar)

        return await ctx.send(f'Items purchased by: {ctx.author.name}', embed=embed)

    if param and (param == 'a' or param == 'all'):
        item_list = ItemList()

        embed = discord.Embed(color=0x1E1E1E, type='rich')
        total = []
        for item in sorted(item_list.items, key=lambda i: i.sell_count, reverse=True):
            if item.sell_count > 0:
                embed.add_field(name=item.name, value=f'Times sold: {item.sell_count}', inline=True)
                total.append(item.value * item.sell_count)
        embed.add_field(name='Total coins raised', value=f'{sum(total)} :coin:', inline=False)

        return await ctx.send('Sell table items:', embed=embed)

    return await ctx.send('Wrong param. See >help ps for usage examples.')
