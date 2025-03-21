import random
from bot.config import Bot
from discord.ext import commands
import asyncio


class Games(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command(name="guess_number", description="Guess the number")
    async def guess_number(self, ctx: commands.Context):
        number = random.randint(1, 20)
        await ctx.send(
            "Welcome to the number guessing game! Guess a number between 0 and 20."
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        tries = 0
        while True:
            try:
                guess = await self.bot.wait_for("message", check=check, timeout=30)
                guess_content = guess.content

                try:
                    guess_number = int(guess_content)
                except ValueError:
                    await ctx.send("Invalid input. Please enter a valid number.")
                    continue

                tries += 1

                if guess_number == number:
                    await ctx.send(
                        f"Congratulations! You guessed the number in {tries} tries."
                    )
                    break
                elif guess_number < number:
                    await ctx.send("Too low! Try again.")
                else:
                    await ctx.send("Too high! Try again.")
            except asyncio.TimeoutError:
                return await ctx.send(
                    f"Time's Up! You didn't guess the number in time. The number was {number}."
                )
            
    @commands.hybrid_command(name="flip", description="flip a coin")
    async def flip(self, interaction: commands.Context):
        random_side = random.randint(0, 1)
        if random_side == 1:
            await interaction.send("Head")
        else:
            await interaction.send("Tail")


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))
