import os

import discord
from discord.ext import commands

from roll_funcs import roll_table

# set bot params
client = commands.Bot(command_prefix=".")
token = os.getenv("GROUP_ROLL_TOKEN")


# notify on bot startup
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Game("Listening to .help"))
    print("I am online")


# add event for group roll table generation
@client.command()
async def get_table(ctx, num, face, mod, dc):
    table = roll_table(num, face, dc, mod)
    await ctx.send("\n".join("{!r}: {!r},".format(k, v)
                   for k, v in table.items()))

if __name__ == '__main__':
    client.run(token)
