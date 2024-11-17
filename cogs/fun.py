import discord
from discord.ext import commands
import requests
import json
import random
import os

with open('config.json') as f:
    config = json.load(f)

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bqotd(self, ctx):
        """Book Quote of the Day"""
        response = requests.get(f"{config['quotable_api_url']}/random?tags=books")
        data = response.json()
        quote = data['content']
        author = data['author']
        await ctx.send(f"**Quote of the Day:**\n{quote}\n- {author}")

    @commands.command()
    async def bqguess(self, ctx):
        """Guess the book from the quote"""
        response = requests.get(f"{config['quotable_api_url']}/random?tags=books")
        data = response.json()
        quote = data['content']
        book = data['tags'][0]  # Assuming the first tag is the book title
        await ctx.send(f"Guess the book for this quote:\n\"{quote}\"")
        
    @commands.command()
    async def bqtheme(self, ctx, *, theme):
        """Fetch quotes based on theme"""
        response = requests.get(f"{config['quotable_api_url']}/random?tags={theme}")
        data = response.json()
        if data:
            quote = data['content']
            author = data['author']
            await ctx.send(f"**{theme.capitalize()} Quote:**\n{quote}\n- {author}")
        else:
            await ctx.send(f"No quotes found for theme: {theme}")

def setup(bot):
    bot.add_cog(Fun(bot))
