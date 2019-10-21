from websocket import create_connection
import time
import requests
import discord
from discord.ext import commands
import asyncio

#commands start with !
client = commands.Bot(command_prefix ='!')

#confiriming bot is ready up
@client.event
async def on_ready():
    print('Bot is ready.')

#running !start starts the script
@client.command()
async def start(ctx):
    #creating connection to blockchain info
    ws = create_connection("wss://ws.blockchain.info/inv")
    ws.send('{"op":"unconfirmed_sub"}')

    #variables
    time1 = time.time()
    price=requests.get("https://blockchain.info/q/24hrprice")
    firstRun=True
    previousHash=""

    #function to grab data
    def grabbingData():
        #obtaining data
        result =  ws.recv()

        #finding hash and value locations in the JSON
        location = result.find('"hash":')
        location2 = result.find('"value":')
        hash=""
        value="";

        #modifying the locations
        location=location+8
        location2=location2+8
        b1=True
        b2=True

        #obtaining full strings and values
        while b1 or b2:
            if result[location] != "\"" and b1:
                hash = hash+result[location]
                location += 1
            elif result[location] == "\"":
                b1=False

            if result[location2]!="," and b2:
                value=value+result[location2]
                location2 += 1
            elif result[location2]==",":
                b2=False

        #editing values
        value = float(value)/100000000.0
        USD = value*float(price.text)

        #printing info
        print("Hash: "+hash)
        print("BTC: "+str(float(value)/100000000.0))
        print("USD: "+str(USD)+"\n")

        #storing and returning list
        output=[hash,value,USD]
        return output

    #running data
    while True:
        output = grabbingData()

        #notify depending on the USD value
        if(output[2]>=1000000 and (str(output[0])!=previousHash or firstRun)):
            await ctx.author.send("{0:,} BTC transaction is on the network. USD value: {1:,.2f} Hash: {2}".format(output[1],output[2],str(output[0])))
            firstRun=False
        #counts to 10 seconds and updates the current BTC price
        end= time.time()
        if (end-time1)>10.0:
            price=requests.get("https://blockchain.info/q/24hrprice")
            time1=time.time()
            print("PRICE UPDATED"+"\n")
        previousHash=output[0]

    ws.close()

#MUST INPUT DISCORD KEY AND CONNECT IT TO A SERVER TO RUN SCRIPT
client.run('')
