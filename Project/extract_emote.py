import requests
from PIL import Image, ImageSequence
from bs4 import BeautifulSoup
import logging

""" Logging configuration """

# logging.basicConfig(level=logging.DEBUG)


""" File paths """

DOWNLOADED_EMOTES_PATH = "downloaded_emotes/"
CONVERTED_EMOTES_PATH = "converted_emotes/"


""" Functions """

def get_emote_id(page_url: str) -> str:
    """ Extract 7TV emote ID from the page_url given """
    emote_id = page_url.split("/")[-1]
    return emote_id


def get_emote_url(emote_id: str) -> str:
    """ Extract the exact emote path from the emote ID given """
    emote_url = f"https://cdn.7tv.app/emote/{emote_id}/4x.webp"
    return emote_url


def download_emote(emote_id: str, emote_url: str) -> str:
    """ Download the (webp) emote with the emote url given, and return its path """

    response = requests.get(emote_url)
    if response.status_code != 200:
        return ""
    downloaded_img_path = f"{DOWNLOADED_EMOTES_PATH}{emote_id}.webp"
    with open(downloaded_img_path, "wb") as img:
        img.write(response.content) # response.content is the image content
    return downloaded_img_path


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


def convert_img(emote_id:str, file_path: str) -> str:
    """ Convert the webp image into a gif, in order to be uploaded to Discord, and return its path. """
    img = Image.open(file_path)
    img.info.pop('background', None) # remove background

    if is_animated(file_path): # check if it's animated
        img_extension = "gif"
    else:
        img_extension = "png"

    converted_img_path = f"{CONVERTED_EMOTES_PATH}{emote_id}.{img_extension}"
    img.save(converted_img_path, save_all=True)
    return converted_img_path


def main(page_url: str) -> str | bool:
    """ Main function. Downloads the image from the given url and converts to either
    a gif (if animated) or a png format (if not animated), returning the file path. """

    try:
        emote_id = get_emote_id(page_url)
        emote_url = get_emote_url(emote_id)
        downloaded_img_path = download_emote(emote_id, emote_url)
        converted_img_path = convert_img(emote_id, downloaded_img_path)
    except:
        return False # if unsuccessful

    return converted_img_path # return file path if the process was successful


if __name__ == "__main__":
    # emote_id = get_emote_id("1234")
    # emote_url = get_emote_url(emote_id)
    # downloaded_img_path = f"{download_emote(emote_id, emote_url)=}"
    # print(downloaded_img_path)

    page_url = "https://7tv.app/emotes/60af769d2c36aae19e32ec9d"
    main(page_url)
