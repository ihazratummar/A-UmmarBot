import asyncio
import os
import discord
import requests
from bot.config import Bot
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime, time
from dotenv import load_dotenv
from ..core.Buttons.buttons import  LinksButton
from pytz import  timezone
from bot.core import times

load_dotenv()

WEATHER_API = os.getenv("WEATHER_API")


class General(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.weekly_task.start()

    @commands.hybrid_command()
    @app_commands.checks.cooldown(1, 10, key=lambda i: i.user.id)
    async def hi(self, interaction: commands.Context):
        await interaction.send(f"Hi how are you")




    @commands.hybrid_command(name="social")
    async def social(self, interaction: commands.hybrid_command):
        embed = discord.Embed(
            title= "Social Links",
            description= "Check Click and Visit Our Official Links for More info!",
            colour= discord.Colour.brand_green()
        )
        embed.set_thumbnail(url="https://media.tenor.com/-Nc9wGWx3X8AAAAi/pepe-fastest-pepe-the-frog.gif")
        embed.set_image(url="https://media1.tenor.com/m/WmU_8UAyg_8AAAAC/night.gif")
        embed.add_field(name="<:discord:1243197853371859017> Discord", value="[Discord](https://discord.gg/DhsEvqHyE9)")
        embed.add_field(name="<:facebook:1243197848498077716> Facebook", value="[Facebook](https://www.facebook.com/crazyforsurprise)")
        embed.add_field(name="<:youtube:1243197856014139485> YouTube", value="[YouTube](https://www.youtube.com/crazyforsurprise)")
        embed.add_field(name="<:instagram:1243197850880446464> Instagram", value="[Instagram](https://www.instagram.com/ihazratummar)")

        button_list = [
            ("Discord", "https://discord.gg/g3M4MWK", "<:discord:1243197853371859017>"),
            ("Facebook", "https://www.facebook.com/crazyforsurprise", "<:facebook:1243197848498077716>"),
            ("YouTube", "https://www.youtube.com/crazyforsurprise", "<:youtube:1243197856014139485>"),
            ("Instagram", "https://www.instagram.com/ihazratummar", "<:instagram:1243197850880446464>")

        ]

        await interaction.send(
            embed= embed, view = LinksButton(buttons_list= button_list)
        )
    @commands.hybrid_command(name="youtube", description="search video")
    async def youtube(self, interaction: commands.Context, search: str):
        response = requests.get(f"https://youtube.com/results?search_query={search}")
        html = response.text
        index = html.find("/watch?v=")
        url = "https://www.youtube.com" + html[index : index + 20]
        await interaction.send(url)

    @tasks.loop(seconds=40)
    async def weekly_task(self):
        target_day = 0  # 0 = Monday, 1 = Tuesday, ..., 6 = Sunday
        target_time = time(hour=16, minute=59)
        local_tz = timezone("Asia/Kolkata")  # Replace with your local timezone

        now = datetime.now(local_tz)
        now_time = now.time()

        if now.weekday() == target_day and now_time.hour == target_time.hour and now_time.minute == target_time.minute:
            print("Condition met!")
            channel = self.bot.get_channel(875192296264593458)
            if channel:
                await channel.send("It's time!")
            else:
                print("Channel not found.")

            next_target_datetime = times.get_next_week_day(now, target_day, target_time, local_tz)
            time_difference = (next_target_datetime - now).total_seconds()-100
            print(f"Next target occurrence: {next_target_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Sleeping for {time_difference} seconds...")
            # Sleep until the next target time
            await asyncio.sleep(time_difference)
        else:
            print(
                f"Condition not met: Now - {now.strftime('%Y-%m-%d %H:%M:%S')}, Target Day - {target_day}, Target Time - {target_time}")

    @weekly_task.before_loop
    async def before_weekly_task(self):
        await self.bot.wait_until_ready()



async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))