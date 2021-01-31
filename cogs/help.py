#Imports
import discord
from discord.ext import commands
from discord.ext.commands import Bot

#Cog Initiation
class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Commands
    @commands.command()
    async def help(self, ctx):
        await ctx.send('This is a help command.')

def setup(client):
    client.add_cog(Help(client))