import discord
from discord.commands import Option
from dotenv import load_dotenv
from utils.logging import log
import os

# Load the env file
load_dotenv()

# Initiate the PyCord Bot.
bot = discord.Bot()


@bot.event
async def on_ready():
    # Log to the user that we're signed in.
    log(4, f"We have logged in as {bot.user}")


# Load the cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.environ["BOT_TOKEN"])
