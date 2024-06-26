import os
import requests
import json
import disnake
from disnake.ext import commands
import config

class Kick(commands.Cog):
    """Responsible for kicking the user out of the game."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="kick")
    async def kick(self, interaction: disnake.Interaction, username: str) -> None:
        url = "https://users.roblox.com/v1/usernames/users"
        data = {"usernames": [username], "excludeBannedUsers": False}

        try:
            res = requests.post(url, json=data)
            res.raise_for_status()

            user_id = json.loads(res.text)['data'][0]['id']
            url = 'https://api.trello.com/1/cards'
            data = {
                'name': str(user_id),
                'idList': config.kick_list,
                'key': os.getenv("TRELLO_API_KEY"),
                'token': os.getenv("TRELLO_TOKEN")
            }

            res = requests.post(url, json=data)
            res.raise_for_status()

            await interaction.send(f"<@{interaction.author.id}>, the user {username} has been kicked, if exists.")

        except (requests.RequestException, KeyError, IndexError, json.JSONDecodeError) as e:
            await interaction.send(f"Failed to kick user {username}. Reason: {str(e)}")
def setup(bot: commands.Bot):
    bot.add_cog(Kick(bot))
