import discord
from discord.ext import commands
import json
import requests

with open('config.json') as f:
    config = json.load(f)

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bugreport(self, ctx, *, report):
        """Report a bug to the admin"""
        log_channel = self.bot.get_channel(int(config['log_channel_id']))
        await log_channel.send(f"Bug Report from {ctx.author}: {report}")
        await ctx.send("Thank you for your report! We'll look into it.")

    @commands.command()
    async def invite(self, ctx):
        """Get the invite link to invite the bot to other servers"""
        invite_url = discord.utils.oauth_url(self.bot.user.id)
        await ctx.send(f"Click here to invite Quotomania to your server: {invite_url}")

   ''' @commands.hybrid_command(
    name="command",
    description="Command description",)
    @app_commands.guilds(discord.Object(id=GUILD_ID)) # Place your guild ID here'''

def setup(bot):
    bot.add_cog(General(bot))
