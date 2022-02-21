from discord.ext import commands
from discord.commands import slash_command, ApplicationContext


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="test")
    async def test(self, ctx: ApplicationContext):
        await ctx.respond("hey lol")


def setup(bot):
    bot.add_cog(Admin(bot))
