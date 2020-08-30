from websocket import create_connection
import time
import requests
import discord
from discord.ext import commands
import asyncio
import BtcNetworkTracker as BTC

#commands start with !
client = commands.Bot(command_prefix ='!')

#confiriming bot is ready up
@client.event
async def on_ready():
    print('Bot is ready.')

#running !start starts the script
@client.command()
async def start(ctx):
    BTC.main()


#MUST INPUT DISCORD KEY AND CONNECT IT TO A SERVER TO RUN SCRIPT
client.run('')
