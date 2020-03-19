"""
This is the simple layout I use whenever creating a new command.
"""

import discord
from discord.ext import commands
import datetime
import random

class New(commands.Cog, name = "New"):
    """
    New Cog
    """
    def __init__(self, bot):
        self.bot = bot
        print("Loaded New Cog.")

    # A simple command format
    @commands.command(name = "SAMPLE", help = "Just a placeholder.", brief = "If parameters then examples here")
    async def sample(self, ctx):
        pass

    # A listener which catches all messages that are not from a Bot user.
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            pass

def setup(bot):
    bot.add_cog(New(bot))
