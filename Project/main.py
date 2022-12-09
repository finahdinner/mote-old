import os
import sys
import discord
from discord.ext import commands, tasks

import extract_emote

""" Bot Info/Prelim. Commands"""

specified_token = '' # add a token in here if you wish to override the default token
if specified_token:
    TOKEN = specified_token
else:
    TOKEN = os.environ.get('RONNIE_PICKERING_TOKEN')

description = "7TVGrabber"
command_prefix = "7tv/"
bot = commands.Bot(command_prefix=command_prefix, description=description, help_command=None, intents=discord.Intents.all())


""" Helper Functions """

def incorrect_command_usage(function_name: str) -> str:
    """ Returns an message for the user when they incorrectly use a command. """

    return f"""ERROR: Correct Usage: **{command_prefix}/{function_name} [URL]**
Make sure not to include too few or too many words or phrases."""


""" Discord Bot Coroutines """

@bot.event
async def on_ready(): # confirms that the bot is online
    print("We have logged in as {0.user}".format(bot))


@bot.command()
async def grab(ctx, *args):

    if len(args) != 1: # if too few or too many args given
        await(ctx.send(incorrect_command_usage(sys._getframe().f_code.co_name)))
        return

    page_url = args[0]

    await(ctx.send(page_url))


bot.run(TOKEN)