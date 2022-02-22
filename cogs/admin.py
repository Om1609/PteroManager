from discord.ext import commands
from discord.commands import slash_command


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # No use for this file yet, I'm just keeping it here because.
    @slash_command(name="test")
    async def test(self, ctx):
        await ctx.respond("hey lol")


def setup(bot):
    bot.add_cog(Admin(bot))
