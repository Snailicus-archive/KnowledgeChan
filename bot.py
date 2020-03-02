import os

import logic

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
    print('o am ready, master')

@bot.command()
async def mewl(ctx):
    await ctx.send('meow!')

@bot.command()
async def combine(ctx, first, second, third):
    await ctx.send(logic.find_confluence(first, second, third))



if __name__ == '__main__':
    logic.pull_essences()
    logic.pull_combinations()

    token = os.environ['secret']
    bot.run(token)
