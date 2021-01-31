import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os
import cogs
import asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

client = commands.Bot(command_prefix = '.', intents = discord.Intents.all())

client.remove_command('help')

@client.event
async def on_ready():
    print('===================================')
    print(f'Logged in as: {client.user.name}')
    print(f'ID: {client.user.id}')
    print(f'Py Lib Version: {discord.__version__}')
    print('===================================')
    game = discord.Game('.help')
    await client.change_presence(status=discord.Status.online, activity=game)

@client.group()
@commands.is_owner()
async def dev(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(':x: The valid subcommands are: `shutdown`, `load`, `unload`, and `reload`.')

@dev.error
async def dev_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        pass

@dev.command()
async def shutdown(ctx):
    await ctx.send('Bot is shutting down.')
    await ctx.bot.logout()
    print('Bot sucessfully shut down.')

@dev.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Cog {extension} has been loaded.')
    
@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(':x: Please specify a cog to load.')

@dev.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Cog {extension} has been unloaded.')

@unload.error
async def unload_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(':x: Please specify a cog to unload.')

@dev.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Cog {extension} has been reloaded!')

@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(':x: Please specify a cog to reload.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Cog {filename[:-3]} has been loaded.')

client.run(TOKEN)