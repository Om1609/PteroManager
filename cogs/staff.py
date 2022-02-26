from discord.ext import commands
import discord
from discord import Embed
import os
from discord.commands import slash_command, Option
from utilities.logging import log
import asyncio


# Define a simple View that gives us a confirmation menu
class Confirm(discord.ui.View):
    def __init__(self, msg: bool):
        super().__init__()
        self.value = None
        self.msg = msg

    # When the confirm button is pressed, set the inner value to `True` and
    # Stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        # await interaction.response.send_message("Confirming", ephemeral=True)
        self.value = True
        for _button in self.children:
            _button.disabled = True
        if not self.msg:  # Checks if a message is ephemeral or not.
            await interaction.message.edit(view=self)
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        for _button in self.children:
            _button.disabled = True
        if not self.msg:
            await interaction.message.edit(view=self)
        self.stop()


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Make the session easier to use.
    @property
    def _session(self):
        return self.bot.http._HTTPClient__session

    # Look up servers
    @slash_command(
        guild_ids=[os.environ["GUILD_ID"]],
        description="Get information about a specified server!",
    )
    async def serverlookup(
        self,
        ctx: discord.ApplicationContext,
        serverid: Option(str, "Server ID"),
        hide: Option(bool, "Hide message?"),
    ):
        roles = [role.name for role in ctx.author.roles]
        if os.environ["ROLE_NAME"] in roles:
            key = os.environ["ADMINS_API_KEY"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
            }
            req = await self._session.get(
                f"https://panel.epikhost.xyz/api/client/servers/{serverid}",
                headers=headers,
            )
            if req.status == 200:
                jsonResponse = await req.json()
                data = {
                    "name": jsonResponse["attributes"]["name"],
                    "id": jsonResponse["attributes"]["identifier"],
                    "node": jsonResponse["attributes"]["node"],
                    "docker_image": jsonResponse["attributes"]["docker_image"],
                    "max_mem": jsonResponse["attributes"]["limits"]["memory"],
                    "max_cpu": jsonResponse["attributes"]["limits"]["cpu"],
                    "max_disk": jsonResponse["attributes"]["limits"]["disk"],
                    "ip": jsonResponse["attributes"]["relationships"]["allocations"][
                        "data"
                    ][0]["attributes"]["ip"],
                    "port": jsonResponse["attributes"]["relationships"]["allocations"][
                        "data"
                    ][0]["attributes"]["port"],
                }
                info_embed = Embed(
                    title=f'Information about: {data["name"]}', color=0xCADCFC
                )
                info_embed.add_field(
                    name="Server Name:", value=data["name"], inline=False
                )
                info_embed.add_field(name="Server ID:", value=data["id"], inline=False)
                info_embed.add_field(name="Node:", value=data["node"], inline=False)
                info_embed.add_field(name="IP:", value=data["ip"], inline=False)
                info_embed.add_field(name="Port:", value=data["port"], inline=False)
                info_embed.add_field(
                    name="Docker Image:", value=data["docker_image"], inline=False
                )
                info_embed.add_field(
                    name="Memory Amount:", value=data["max_mem"], inline=False
                )
                info_embed.add_field(
                    name="CPU Amount:", value=data["max_cpu"], inline=False
                )
                info_embed.add_field(
                    name="Memory Amount:", value=data["max_disk"], inline=False
                )
            else:
                info_embed = Embed(
                    title="Error",
                    description=f"Sorry, {ctx.author.name}, but the server {serverid} doesn't exist or the panel is down!",
                    color=0xFF0033,
                )
            await ctx.respond(embed=info_embed, ephemeral=hide)
        else:
            log(
                3,
                f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) attempt to run the Server Lookup command!",
            )
            embed = Embed(
                title="Error",
                description=f"Sorry, {ctx.author.name}, but you don't have permission to run this command!",
                color=0xFF0033,
            )
            await ctx.respond(embed=embed, ephemeral=True)

    # Delete a server
    @slash_command(
        guild_ids=[os.environ["GUILD_ID"]],
        description="Delete a specified server!",
    )
    async def deleteserver(
        self,
        ctx: discord.ApplicationContext,
        serverid: Option(str, "Server ID"),
        hide: Option(bool, "Hide message?"),
    ):
        roles = [role.name for role in ctx.author.roles]
        if os.environ["ROLE_NAME"] in roles:
            key = os.environ["ADMINS_API_KEY"]
            # await ctx.respond(f"Looking up {serverid}!", ephemeral=True)
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
            }
            req = await self._session.get(
                f"https://panel.epikhost.xyz/api/client/servers/{serverid}",
                headers=headers,
            )
            if req.status == 200:
                jsonResponse = await req.json()
                data = {
                    "name": jsonResponse["attributes"]["name"],
                    "id": jsonResponse["attributes"]["identifier"],
                    "node": jsonResponse["attributes"]["node"],
                    "docker_image": jsonResponse["attributes"]["docker_image"],
                    "max_mem": jsonResponse["attributes"]["limits"]["memory"],
                    "max_cpu": jsonResponse["attributes"]["limits"]["cpu"],
                    "max_disk": jsonResponse["attributes"]["limits"]["disk"],
                    "ip": jsonResponse["attributes"]["relationships"]["allocations"][
                        "data"
                    ][0]["attributes"]["ip"],
                    "port": jsonResponse["attributes"]["relationships"]["allocations"][
                        "data"
                    ][0]["attributes"]["port"],
                    "internalid": jsonResponse["attributes"]["internal_id"],
                }
                info_embed = Embed(
                    title=f'Information about: {data["name"]}', color=0xCADCFC
                )
                info_embed.add_field(
                    name="Server Name:", value=data["name"], inline=False
                )
                info_embed.add_field(name="Server ID:", value=data["id"], inline=False)
                info_embed.add_field(name="Node:", value=data["node"], inline=False)
                info_embed.add_field(name="IP:", value=data["ip"], inline=False)
                info_embed.add_field(name="Port:", value=data["port"], inline=False)
                info_embed.add_field(
                    name="Docker Image:", value=data["docker_image"], inline=False
                )
                info_embed.add_field(
                    name="Memory Amount:", value=data["max_mem"], inline=False
                )
                info_embed.add_field(
                    name="CPU Amount:", value=data["max_cpu"], inline=False
                )
                info_embed.add_field(
                    name="Memory Amount:", value=data["max_disk"], inline=False
                )
                info_embed.add_field(
                    name="MAKE SURE!",
                    value="\n\nENSURE THAT THIS IS THE SERVER YOU WANT TO DELETE, THIS IS NOT REVERSABLE!",
                    inline=False,
                )
            else:
                info_embed = Embed(
                    title="Error",
                    description=f"Sorry, {ctx.author.name}, but the server {serverid} doesn't exist or the panel is down!",
                    color=0xFF0033,
                )
            view = Confirm(msg=hide)
            await ctx.respond(embed=info_embed, ephemeral=hide, view=view)
            await view.wait()
            if view.value is None:
                await ctx.respond("Timed out! Cancelling.", ephemeral=hide)
            elif view.value is True:
                await ctx.respond("Confirmed! Going ahead now.", ephemeral=hide)
                admin_key = os.environ["PTERO_ADMIN_KEY"]
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {admin_key}",
                }
                var = data["internalid"]
                req = await self._session.delete(
                    f"https://panel.epikhost.xyz/api/application/servers/{var}/force",
                    headers=headers,
                )
                await asyncio.sleep(1.5)
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {key}",
                }
                req = await self._session.get(
                    f"https://panel.epikhost.xyz/api/client/servers/{serverid}",
                    headers=headers,
                )
                if req.status == 200:
                    await ctx.respond(
                        "Failed to delete. Please try again later.",
                        ephemeral=hide,
                    )
                else:
                    await ctx.respond(
                        "Success! Deleted the server!",
                        ephemeral=hide,
                    )
            else:
                await ctx.respond("Cancelled! Stopping.", ephemeral=hide)

        else:
            log(
                3,
                f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) attempt to run the Delete Server command!",
            )
            embed = Embed(
                title="Error",
                description=f"Sorry, {ctx.author.name}, but you don't have permission to run this command!",
                color=0xFF0033,
            )
            await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Staff(bot))
