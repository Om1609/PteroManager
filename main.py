from dotenv import load_dotenv
from utilities.bot import PteroManager
from utilities import logging
import os

# Clear the console at the start so it's nice and clean for errors and the start message.
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

# Load the env file
load_dotenv()

# Initiate the Bot from the utils file.
bot = PteroManager()

# Attempt to load the cogs.
try:
    bot.load_cogs()
    logging.log(4, "Loaded all cogs successfully!!")
except:
    logging.log(1, "Error in loading cogs. Bot will not start.")
    exit()

# Attempt to run the bot.
try:
    bot.run(os.environ["BOT_TOKEN"])
except:
    logging.log(
        1,
        "Bot failed to start. Check the token and your network connection then try again!",
    )