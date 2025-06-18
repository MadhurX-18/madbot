from discord.ext import commands
import random

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hey there! 😄")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! 🏓 {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def flip(self, ctx):
        await ctx.send(f"🪙 {random.choice(['Heads', 'Tails'])}!")

async def setup(bot):
    await bot.add_cog(General(bot))