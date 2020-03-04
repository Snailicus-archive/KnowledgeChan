import os
import re
from pprint import pformat

import discord
from discord.ext import commands

import logic

# TODO: allow listing combinations by essence

ADMIN_ROLES = 'Magic Society Official', 'Admin', 'Author'
HELPSTRING = """**```Standard command list```**
Use `?command` to use a command.

__**Accessible by all**__:
**0.** **`?help`**
	prints this.

**1.** **`?combine essence1 essence2 essence3`**
	prints the confluence

**2.** **`?list combinations`**
	upload combinations database(csv file)

**3.** **`?list combinations confluence_name`**
	prints all the combinations leading to confluence

**4.** **`?list essences`**
	uploads essences database(csv file)

__**Accessible only by  *Author* ,  *Owner*  and  *Magic Society Official*  roles**__:
**5.** **`?new essence name [rarity]`**
	add new essence to database. rarity is optional

**6.** **`?new combination essence1 essence2 essence3 confluence`**
	adds a new combination to the database
	creates new confluence if it doesnt exist

When there's trouble you know who to call.(lynx...)"""

# this is a global. an intentional one.
bot = commands.Bot(command_prefix='?')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('o am ready, master')

@bot.command()
async def help(ctx):
    await ctx.send(HELPSTRING)

@bot.command()
async def mewl(ctx):
    await ctx.send('meow!')


@bot.command()
async def combine(ctx, a, b, c):
    con, comb = logic.find_confluence(a, b, c)
    print(logic.find_confluence(a, b, c))
    await ctx.send(f'`{logic.show_combination(comb)} -> {con.name}`')

@combine.error
async def combine_error(ctx, error):
    message = 'Wot?'
    if isinstance(error, commands.MissingRequiredArgument):
        message = 'List 3 essences.'
    elif isinstance(error, commands.CommandInvokeError):
        err = error.original
        if isinstance(err, NameError):
            message = f"Essence {str(err)} doesn't exist."
        if isinstance(err, IndexError):
            message = 'list 3 essences.'
    await ctx.send(f'**ERROR**: `{message}`')
    print(error)

@bot.command()
async def list(ctx, what, name=''):
    what = what.lower()
    name = logic.form(name)
    if what in ('conf', 'confluences', 'combination', 'combinations'):
        # list confluences
        await list_confluences(ctx, name)
    elif what in ('essences',):
        await list_essences(ctx)
    else:
        raise commands.MissingRequiredArgument

async def list_confluences(ctx, name=None):
    if name:
        await ctx.send(logic.confluences[name])
    else:
        with open(logic.COMBINATIONS_FILE, 'rb') as f:
            await ctx.send('Included in file', file=discord.File(f, filename='combinations.csv'))

async def list_essences(ctx):
    with open(logic.ESSENCES_FILE, 'rb') as f:
        await ctx.send('Included in file', file=discord.File(f, filename='essences.csv'))

@list.error
async def list_error(ctx, error):
    message = 'Wot?'
    if isinstance(error, commands.MissingRequiredArgument):
        message = 'List confluences or essences.'
    elif isinstance(error, commands.CommandInvokeError):
        err = error.original
        if isinstance(err, KeyError):
            message = "Not found."
    await ctx.send(f'**ERROR**: `{message}`')

    print(error)

# TODO: add "new" command line "list"
@bot.command()
@commands.check_any(commands.has_any_role(*ADMIN_ROLES), commands.is_owner())
async def new(ctx, what, *args):
    what = what.lower()
    if what == 'essence':
        await new_essence(ctx, *args)
    elif what == 'combination':
        await new_combination(ctx, *args)
    else:
        raise commands.MissingRequiredArgument

async def new_essence(ctx, name, rarity='Unknown'):
    name, rarity = map(logic.form, [name, rarity])
    logic.add_essence(name, rarity)
    await ctx.send(f'Added new essence `{name} [{rarity}]`.')


# TODO: allow syntax as   a + b + c -> thing
async def new_combination(ctx, a, b, c, name):
    a, b, c = map(logic.form, [a, b, c])
    logic.add_combination(a, b, c, name)
    await ctx.send(f'Added combination `{a} + {b} + {c} -> {name.lower().capitalize()}`')

@new.error
async def new_error(ctx, error):
    message = "I don't understand Q_Q"
    if isinstance(error, commands.CheckFailure):
        message = 'You are unworthy... Authorized personnel only.'
    if isinstance(error, commands.MissingRequiredArgument):
        message = 'Please add either new essence or new combination.'
    elif isinstance(error, commands.CommandInvokeError):
        err = error.original
        if isinstance(err, NameError):
            message = f'Essence {str(err)} is unrecognized.'
        elif isinstance(err, IndexError):
            message = 'Essences must be unique in combination'
        elif isinstance(err, KeyError):
            message = 'Its already a thing...'

    await ctx.send(f'**ERROR**: `{message}`')
    print(error)


if __name__ == '__main__':
    logic.pull_essences()
    logic.pull_combinations()

    token = os.environ['secret']
    bot.run(token)
