import os
import sys
import discord
from discord.ext import commands, tasks

import extract_emote


""" Logging configuration """
from for_logging import MyLogger
from pathlib import Path
file_name = Path(__file__).stem # get name of the current file (without the .py)
# Usage: my_logger.logger.[LEVEL]('[LOG MESSAGE]')
my_logger = MyLogger(file_name=file_name, log_file_path=f"logs/{file_name}.log") # create an instance of MyLogger


""" Bot Info/Prelim. Commands"""

specified_token = '' # add a token in here if you wish to override the default token
if specified_token:
    TOKEN = specified_token
else:
    TOKEN = os.environ.get('RONNIE_PICKERING_TOKEN')

description = "7TVGrabber"
command_prefix = "bants/"
bot = commands.Bot(command_prefix=command_prefix, description=description, help_command=None, intents=discord.Intents.all())


""" Helper Functions """

def incorrect_command_usage(function_name: str) -> str:
    """ Returns an message for the user when they incorrectly use a command. """

    return f"""ERROR: Incorrect Usage. 
- **{command_prefix}{function_name} [url] [name]**
- Providing your own custom **[name]** is *optional*, but will speed up the process."""


""" Discord Bot Coroutines """

@bot.event
async def on_ready(): # confirms that the bot is online
    print("We have logged in as {0.user}".format(bot))


@bot.command()
async def grab(ctx, *args):

    if len(args) != 1 and len(args) != 2: # if too few or too many args given
        await(ctx.send(incorrect_command_usage(sys._getframe().f_code.co_name)))
        return

    page_url = args[0]
    if len(args) == 2: # if a name is provided
        name_given = args[1]
        # download the correct emote for discord, and later uploading to the server with the name given (name_given)
        emote_name, discord_img_path, error_message = extract_emote.main(page_url=page_url, name_given=name_given)
    else: # no name is given - will use the default 7TV name
        # download the correct emote for discord, and return the default 7TV name
        emote_name, discord_img_path, error_message = extract_emote.main(page_url=page_url, name_given="")

    if not discord_img_path: # if the image extraction failed
        await(ctx.send(error_message)) # send the error message that was returned
        return

    await(ctx.send(f"""Success - {emote_name} retrieved.
Sorry I take so long. :older_man:"""))

    my_logger.logger.debug('SUCCESS - Image uploaded to the server.')


bot.run(TOKEN)