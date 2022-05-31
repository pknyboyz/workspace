#import the packages
import discord
from dotenv import load_dotenv
import os

#load .env file and replace your token in Token varaible
load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg=message.content
    if '+recon' in msg:
        url = str.strip(msg.split("+recon",1)[1])
        f = open("out.txt", "r+")
        f.seek(0)
        f.truncate()
        await message.channel.send("Scanning Started on : "+url)
        stream = os.popen("subfinder -d "+url+" -silent -o out.txt")
        output = stream.read()
        await message.channel.send("Your result:- \n")
        await message.channel.send(file=discord.File("out.txt"))
    else:
        await message.channel.send("Wrong command")
        

client.run(TOKEN)
