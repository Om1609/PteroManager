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

# Load the cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.environ["BOT_TOKEN"])
