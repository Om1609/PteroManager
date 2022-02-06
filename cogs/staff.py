from discord.ext import commands
import discord
from discord import Embed
import os
from discord.commands import slash_command, Option
from utils.logging import log
import requests

class Staff(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @slash_command(
      guild_ids=[os.environ["GUILD_ID"]],
      description="Get information about a specified server!",
      )
  async def serverlookup(
      self,
      ctx: discord.ApplicationContext,
      serverid: discord.commands.Option(str, "Server ID"),
      hide: discord.commands.Option(bool, "Hide message?"),
  ):
    roles = [role.name for role in ctx.author.roles]
    if os.environ["ROLE_NAME"] in roles:
      if hide == True:
        key = os.environ["ADMINS_API_KEY"]
        # await ctx.respond(f"Looking up {serverid}!", ephemeral=True)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
        req = requests.get(f'https://panel.epikhost.xyz/api/client/servers/{serverid}', headers=headers)
        jsonResponse = req.json()
        data = {
          "name": jsonResponse["attributes"]["name"]
        }
        info_embed = Embed(title=f'Information about: {data["name"]}')
        info_embed.add_field(
          name = "Server Name:",
          value = data["name"],
          inline=True
        )
        await ctx.send(embed=info_embed)

      else:
        await ctx.respond(f"Looking up {serverid}!")
    else:
      log(3, f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) attempt to run the Server Lookup command!")
      await ctx.respond(f"Sorry, {ctx.author.name}, but you don't have permission to run this command!", ephemeral=True)


def setup(bot):
  bot.add_cog(Staff(bot))