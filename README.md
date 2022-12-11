# Mote, a Discord bot

### Video Demo: https://youtu.be/kxIsNeCQlGc
### Description:

**Mote is a Discord bot designed to help you with uploading 7TV emotes to your Discord server.<br><br>**
It works with *7tv.app*, a website/browser extension acting as a database for emotes, which was designed for *twitch.tv*.<br>
The bot is coded in Python, and uses the *discord.py* library for its bot-related functions.<br>
Some of the additional libraries and modules used: *PIL*, *requests*, *selenium* and in-built modules such as *logging*, *os* and *sys*.

**File Breakdown**
- **bot.py** runs the main bot-related functions, including:
  - Initiating/logging-in the bot, using the bot *token* which is stored as an environment variable
  - Defining the bot prefix (*mote/*) and bot functions (*/grab* and */help*)
  - Within the */grab* function definition, there is logic that checks to see if a URL is provided, as well as a check for if the user has the necessary permissions to use the command.
  - After *extract_emote.py* downloads the emote from the website, some lines in *bot.py* are responsible for uploading to emote to the Discord server, and confirming to the user that it was successful (or not successful).
 
- **extract_emote.py** is responsible for extracting the emote from the *7tv* website.
  - The emote's ID (as defined on the 7tv website) is extracted from the URL, and if no name was provided by the user, the emote's name is extracted as well.
  - *Selenium* is used to render the page URL, if the user did not provide an emote name. Selenium is used rather than just a barebones *request*, because the majority of the page content (including the emote's name) is rendered using JavaScript, and I couldn't find another library to render this information in a more lightweight manner.
  - *PIL* is used to check if the .webp file is animated or not. If it is animated, the .gif version is downloaded, and if not animated, the .png version is downloaded.
  - At the end of the script, various return values are provided, including the file path of the downloaded emote (in its proper gif/png format). These return values are used in *bot.py* to upload the file to the Discord server.

- **for_logging.py**
  - For developer use, but this file provides a class definition for a *logger*, which is used to log *debug* and *error* lines at various points in the code.

**Bot Usage:**

- *mote/grab [7tv-url] [emote-name]* -- retrieves the emote from the 7tv URL provided, and uploads to the current discord server
- *mote/help* -- provides usage information<br>

**Discord Permissions Required:**
- Send Messages
- Manage Emojis and Stickers

**Additional notes:**
- Emoji uploads to a server may only be conducted by someone with sufficient privileges to do so
- *requirements.txt*, located in the *Projects* folder, is for installing the necessary dependencies for this project, ideally into a virtual environment.
