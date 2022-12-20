import os
import discord
from discord.ext import commands, tasks
import discord

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
    TOKEN = os.environ.get('MOTE_BOT_TOKEN')

description = "7TVGrabber"
command_prefix = "mote/"
bot = commands.Bot(command_prefix=command_prefix, description=description, help_command=None, intents=discord.Intents.all())
invite_link = "https://discord.com/api/oauth2/authorize?client_id=1050507549486620764&permissions=1073743872&scope=bot"

""" Helper Functions """

def incorrect_command_usage(function_name: str) -> str:
    """ Returns an message for the user when they incorrectly use a command. """

    if function_name == "grab":
        return f"""ERROR: Incorrect Usage. 
    - **{command_prefix}{function_name} [7tv-url] [emote-name]**
    - Providing your own custom (alphanumeric) [emote-name] is *optional*, but will speed up the grabbing process."""
    elif function_name == "convert":
            return f"""ERROR: Incorrect Usage. 
    - **{command_prefix}{function_name} [emote-name]**, with a **png/jpg/jpeg** image attached."""

    return "ERROR: Incorrect Usage."

""" Discord Bot Coroutines """

@bot.event
async def on_ready(): # confirms that the bot is online
    print("We have logged in as {0.user}".format(bot))


@bot.command()
async def grab(ctx, *args):

    has_emoji_perms = ctx.message.author.guild_permissions.manage_emojis
    if has_emoji_perms is False:
        await(ctx.send("You do not have sufficient permissions to use this command."))
        return

    if len(args) != 1 and len(args) != 2: # if too few or too many args given
        await(ctx.send(incorrect_command_usage("grab")))
        return

    page_url = args[0]
    if len(args) == 2: # if a name is provided
        name_given = args[1]
        if not name_given.isalnum(): # if the name isn't fully alphanumeric
            await(ctx.send("Choose another emote name - it must be **fully** alphanumeric."))
            return
        bot_message = await(ctx.send("Extracting emoji info, bear with me..."))
        # download the correct emote for discord, and later uploading to the server with the name given (name_given)
        emote_name, discord_img_path, error_message = extract_emote.main_grab(page_url=page_url, name_given=name_given, img_size_7tv=4)
    else: # no name is given - will use the default 7TV name
        bot_message = await(ctx.send("Extracting emoji info, bear with me..."))
        # download the correct emote for discord, and return the default 7TV name
        emote_name, discord_img_path, error_message = extract_emote.main_grab(page_url=page_url, name_given="", img_size_7tv=4)

    if not discord_img_path: # if the image extraction failed
        await bot_message.edit(content=error_message) # send the error message that was returned
        return

    # upload emoji to the server
    img_size_7tv = 4 # 7tv image size values vary from 1x to 4x
    while img_size_7tv >= 1:

        try: # try to upload the image
            with open(discord_img_path, "rb") as f:
                image = f.read()
            await ctx.guild.create_custom_emoji(name=emote_name, image=image)

        except discord.errors.HTTPException as e: # if image is too large
            my_logger.logger.debug(f'Failed to upload size {img_size_7tv} - {e}')
            # try to download the next smallest emote, returning a new img path each time
            if img_size_7tv == 1: # to prevent img_size_7tv reaching 0, because 0x doesn't exist
                break
            img_size_7tv -= 1 # for the next iteration below
            my_logger.logger.debug(f'Trying: {img_size_7tv=}')
            await bot_message.edit(content=f"Image file too large - trying smaller versions (Size: {img_size_7tv})...")
            emote_name, discord_img_path, error_message = extract_emote.main_grab(page_url=page_url, name_given=emote_name, img_size_7tv=img_size_7tv)
            if not discord_img_path: # if an error
                await bot_message.edit(content=error_message) # send the error message that was returned
                return

        else: # if successfully uploaded
            await bot_message.edit(content=f"Success - **{emote_name}** grabbed!")
            my_logger.logger.debug('**SUCCESS!** Emoji uploaded to the server.')
            return

    await bot_message.edit(content="ERROR: Could not find a suitably-sized emote with the URL provided.")


@bot.command()
async def convert(ctx, image_file: discord.Attachment | None, *args):

    has_emoji_perms = ctx.message.author.guild_permissions.manage_emojis
    if has_emoji_perms is False:
        await(ctx.send("You do not have sufficient permissions to use this command."))
        return

    if image_file is None:
        await(ctx.send("You must attach an image! Unfortunately, embedded image links won't work."))
        return

    if len(args) != 1:
        await(ctx.send(incorrect_command_usage("convert")))
        return

    name_given = args[0] # emote name specified
    bot_message = await(ctx.send("Extracting emoji info, bear with me..."))
    # download image and resize if necessary
    img_path, img_size, error_message = extract_emote.main_convert(image_file.url, name_given=name_given)
    if not img_path: # if .main_convert wasn't successful
        await(bot_message.edit(content=error_message))
        return
    
    try:
        with open(img_path, "rb") as f:
            image = f.read()
        await ctx.guild.create_custom_emoji(name=name_given, image=image)

    except discord.errors.HTTPException as e:
        my_logger.logger.debug(f'Failed to upload {name_given} - size {img_size} - {e}')
        await bot_message.edit(content="ERROR: Failed to upload emote to the server.") # send the error message that was returned
        return

    else: # if successfully uploaded
        await bot_message.edit(content=f"Success - **{name_given}** uploaded!")
        my_logger.logger.debug('**SUCCESS!** Emoji uploaded to the server.')
        return


@bot.command()
async def invite(ctx):
    await(ctx.send(f"Invite link: {invite_link}"))


@bot.command()
async def help(ctx):

    has_emoji_perms = ctx.message.author.guild_permissions.manage_emojis
    if has_emoji_perms is False:
        no_perms = f"**__To use {command_prefix}grab, you must have permission to manage emojis.__**"
    else:
        no_perms = ""

    await(ctx.send(f"""Usage: **{command_prefix}grab [7tv-url] [emote-name]**
Providing your own (alphanumeric) [emote-name] is *optional*, but will speed up the grabbing process.
{no_perms}"""))


bot.run(TOKEN)