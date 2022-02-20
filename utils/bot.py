import discord

class PteroManager(discord.Bot):
    def __init__(self):
        super().__init__(
            intents=discord.Intents.default(),
            allowed_mentions=discord.AllowedMentions.none()
        )
        
    async def on_ready(self):
        # Log to the user that we're signed in
        log(4, f"We have logged in as {self.user}")
