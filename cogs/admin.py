from discord.ext import commands
from discord.commands import slash_command

class Admin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @slash_command(name="test")
  async def test(self, ctx):
    await ctx.respond()

def setup(bot):
  bot.add_cog(Admin(bot))