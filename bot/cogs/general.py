import asyncio
import discord
import re
import requests
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from bot import openai_client, WEATHER_API
from bot.config import Bot
from ..core.Buttons.buttons import LinksButton
from ..core.openai_utils import get_chat_completion


class General(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command()
    @app_commands.checks.cooldown(1, 10, key=lambda i: i.user.id)
    async def hi(self, interaction: commands.Context):
        await interaction.send(f"Hi how are you")


    @commands.hybrid_command(name="youtube", description="search video")
    async def youtube(self, interaction: commands.Context, search: str):
        response = requests.get(f"https://youtube.com/results?search_query={search}")
        html = response.text
        index = html.find("/watch?v=")
        url = "https://www.youtube.com" + html[index : index + 20]
        await interaction.send(url)

    @commands.hybrid_command(name="love", description="Get a beautiful Islamic love quote ❤️")
    async def love(self, interaction: commands.Context):
        await interaction.defer()
        prompt = (
            "Create a heartfelt and beautiful Islamic love quote or line for us husband and wife.ismita and ummar "
            "It should reflect Islamic values of love, compassion, and respect in marriage. "
            "Avoid sounding robotic. Make it emotional, poetic, and include relevant emojis."
        )
        system_prompt = (
            "You are a helpful assistant that generates emotionally touching Islamic love quotes. "
            "Do not reword any proper names or keywords. "
            "The quote should be elegant, not exceed 950 characters, include emojis, and must feel human and heartfelt. "
            "Output only the quote. No explanations, no prefixes."
        )
        summary = get_chat_completion(prompt=prompt, system=system_prompt)
        embed = discord.Embed(title="Love Quote", description=summary, color=0x00FFFF)
        await interaction.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
