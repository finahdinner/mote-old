from PIL import Image, ImageSequence
import requests

""" Logging configuration """
from for_logging import MyLogger
from pathlib import Path
file_name = Path(__file__).stem # get name of the current file (without the .py)
# Usage: my_logger.logger.[LEVEL]('[LOG MESSAGE]')
my_logger = MyLogger(file_name=file_name, log_file_path=f"logs/{file_name}.log") # create an instance of MyLogger


""" File paths """

DOWNLOADED_EMOTES_PATH = "downloaded_emotes/"
DISCORD_EMOTES_PATH = "discord_emotes/"


""" Functions """

def get_emote_id(page_url: str) -> str:
    """ Extract 7TV emote ID from the page_url given """
    emote_id = page_url.split("/")[-1]
    my_logger.logger.debug(f'{emote_id=}')
    return emote_id


def get_emote_url(emote_id: str) -> str:
    """ Extract the exact emote path from the emote ID given """
    emote_url = f"https://cdn.7tv.app/emote/{emote_id}/4x.webp"
    my_logger.logger.debug(f'{emote_url=}')
    return emote_url


def download_emote(emote_id: str, emote_url: str, img_type: str = "webp") -> str:
    """ Download the (webp) emote with the emote url given, and return its path """

    response = requests.get(emote_url)
    if response.status_code != 200:
        return ""
    # img type is webp by default, but can also be gif or png
    if img_type == "webp": # if the download is webp, this is because we're downloading to check if animated
        img_path = f"{DOWNLOADED_EMOTES_PATH}{emote_id}.{img_type}"
    else: # ie if gif or png - this means we are downloading the type for discord
        img_path = f"{DISCORD_EMOTES_PATH}{emote_id}.{img_type}"

    with open(img_path, "wb") as img:
        img.write(response.content) # response.content is the image content
    my_logger.logger.debug(f'SUCCESS - Downloaded Image. Path = {img_path}.')

    return img_path


def is_animated(img_path: str) -> bool:
    """ Checks if webp image is animated or not. """
    media_file = Image.open(img_path)
    # counting the number of frames. if frames > 1, it is animated
    index = 0
    for _ in ImageSequence.Iterator(media_file):
        index += 1
    if index > 1:
        return True
    else:
        return False


def discord_img(emote_id:str, file_path: str, emote_url_webp: str) -> str:
    """ Convert the webp image into a gif, in order to be uploaded to Discord, and return its path. """

    try: # big try-except block, I know this is bad practice!
        img = Image.open(file_path)
        img.info.pop('background', None) # remove background

        if is_animated(file_path): # check if it's animated.
            img_type = 'gif'
        else:
            img_type = 'png'

        discord_emote_url = emote_url_webp.replace('4x.webp', f'4x.{img_type}') # generate the correct png or gif url
        discord_img_path = download_emote(emote_id=emote_id, emote_url=discord_emote_url, img_type=img_type)
        if not discord_img_path: # if it can't navigate to the page
            return ""
        my_logger.logger.debug(f'SUCCESS - Discord Image Downloaded. Path = {discord_img_path}.')

    except:
        return ""
    
    return discord_img_path


def main(page_url: str) -> str | bool:
    """ Main function. Downloads the image from the given url and converts to either
    a gif (if animated) or a png format (if not animated), returning the file path. """

    emote_id = get_emote_id(page_url) # get emote id from the given page url
    emote_url_webp = get_emote_url(emote_id) # get webp img url
    downloaded_img_path = download_emote(emote_id=emote_id, emote_url=emote_url_webp, img_type="webp") # download webp image
    if not downloaded_img_path: # if it failed to find the url
        my_logger.logger.error(f'Emote URL for --{page_url}-- not found.')
        return False
    discord_img_path = discord_img(emote_id=emote_id, file_path=downloaded_img_path, emote_url_webp=emote_url_webp)
    if not discord_img_path: # if it failed to load the downloaded file
        my_logger.logger.error(f'Failed to download Discord image for --{page_url}--.')
        return False

    return discord_img_path # return file path if the process was successful


if __name__ == "__main__":
    page_url = "https://7tv.app/emotes/60abf171870d317bef23d399" # test url
    main(page_url)