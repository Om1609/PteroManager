import json
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

    @property
    def _session(self):
        return self.bot.http._HTTPClient__session

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
            if hide == True:
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
                jsonResponse = await req.json()
                data = {
                    "name": jsonResponse["attributes"]["name"],
                    "id": jsonResponse["attributes"]["identifier"],
                    "node": jsonResponse["attributes"]["node"],
                    "docker_image": jsonResponse["attributes"]["docker_image"],
                    "max_mem": jsonResponse["attributes"]["limits"]["memory"],
                    "max_cpu": jsonResponse["attributes"]["limits"]["cpu"],
                    "max_disk": jsonResponse["attributes"]["limits"]["disk"],
					"ip": jsonResponse["attributes"]["relationships"]["allocations"]["data"][0]["attributes"]["ip"],
					"port": jsonResponse["attributes"]["relationships"]["allocations"]["data"][0]["attributes"]["port"]
                }
                info_embed = Embed(
                    title=f'Information about: {data["name"]}', color=0xCADCFC
                )
                info_embed.add_field(
                    name="Server Name:", value=data["name"], inline=False
                )
                info_embed.add_field(
					name="Server ID:", value=data["id"], inline=False
				)
                info_embed.add_field(
					name="Node:", value=data["node"], inline=False
				)
                info_embed.add_field(
                    name="IP:", value=data["ip"], inline=False
                )
                info_embed.add_field(
                    name="Port:", value=data["port"], inline=False
                )
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
                await ctx.respond(embed=info_embed)

            else:
                await ctx.respond(f"Looking up {serverid}!")
        else:
            log(
                3,
                f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) attempt to run the Server Lookup command!",
            )
            await ctx.respond(
                f"Sorry, {ctx.author.name}, but you don't have permission to run this command!",
                ephemeral=True,
            )


def setup(bot):
    bot.add_cog(Staff(bot))
