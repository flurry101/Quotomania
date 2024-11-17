import discord
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shutdown(self, ctx):
        """Shuts down the bot"""
        if ctx.author.id == 1234567890:  # Replace with the bot owner's Discord ID
            await ctx.send("Shutting down...")
            await self.bot.close()
        else:
            await ctx.send("You don't have permission to shut down the bot.")

def setup(bot):
    bot.add_cog(Owner(bot))
