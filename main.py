import discord
from discord.commands import Option
from dotenv import load_dotenv
from utils.logging import log
from utils.bot import PteroManager
import os

# Load the env file
load_dotenv()

# Initiate the PyCord Bot.
bot = PteroManager()
try:
    bot.load_cogs()
    print("Loaded all cogs")
except:
    print("There was an error in loading the cogs!")

bot.run(os.environ["BOT_TOKEN"])
