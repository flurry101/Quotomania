import discord
from discord.ext import commands
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import random
import io

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

    @commands.command()
    async def bqsearch(self, ctx, *, query):
        """Search for a given book quote"""
        response = requests.get(f"{config['quotable_api_url']}/search", params={"query": query})
        data = response.json()
        if data['results']:
            quote = data['results'][0]['content']
            author = data['results'][0]['author']
            await ctx.send(f"Found Quote:\n{quote}\n- {author}")
        else:
            await ctx.send("No results found for your search.")

    @commands.command()
    async def bq_analyze(self, ctx, *, quote):
        """Analyze the meaning or significance of a quote from a book"""
        # For the sake of simplicity, we'll use a basic sentiment analysis
        # You can integrate more advanced NLP tools like OpenAI, Hugging Face, or any other model for deep analysis
        sentiment = self.analyze_sentiment(quote)  # Let's assume a basic sentiment analysis function
        await ctx.send(f"Analysis of quote: '{quote}'\nSentiment: {sentiment}")

    def analyze_sentiment(self, quote):
        """Simple sentiment analysis function (can be replaced with a more advanced one)"""
        positive_keywords = ["love", "inspire", "hope", "bravery", "strength"]
        negative_keywords = ["hate", "despair", "weak", "fear", "pain"]

        sentiment_score = 0
        for word in positive_keywords:
            if word in quote.lower():
                sentiment_score += 1
        for word in negative_keywords:
            if word in quote.lower():
                sentiment_score -= 1
        
        if sentiment_score > 0:
            return "Positive"
        elif sentiment_score < 0:
            return "Negative"
        else:
            return "Neutral"

    @commands.command()
    async def bqwallpaper(self, ctx, *, quote=None):
        """Generate an image with a book quote formatted for wallpaper or social media"""
        if quote is None:
            quote = "A book is a dream that you hold in your hands."
        
        # Get a random author
        authors = ["Mark Twain", "J.K. Rowling", "George Orwell", "Jane Austen", "Leo Tolstoy"]
        author = random.choice(authors)
        
        # Create wallpaper image
        image = self.generate_wallpaper(quote, author)
        
        # Save the image to a BytesIO object to send it as an attachment
        with io.BytesIO() as image_binary:
            image.save(image_binary, format="PNG")
            image_binary.seek(0)
            await ctx.send(file=discord.File(image_binary, "quote_wallpaper.png"))

    def generate_wallpaper(self, quote, author):
        """Generates a wallpaper image with the quote and author"""
        img = Image.new('RGB', (800, 600), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        # Adding text to the image
        text = f"\"{quote}\""
        author_text = f"- {author}"

        # Position the text in the center
        draw.text((20, 50), text, font=font, fill=(0, 0, 0))
        draw.text((20, 500), author_text, font=font, fill=(0, 0, 0))

        return img

def setup(bot):
    bot.add_cog(Fun(bot))
