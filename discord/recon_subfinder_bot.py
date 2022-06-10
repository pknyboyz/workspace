#import the packages
import discord
from dotenv import load_dotenv
import os
import subprocess

#load .env file and replace your token in Token varaible
load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


# A decorator that tells the client to run the function below it when a certain event happens.
@client.event
async def on_message(message):
    """
    If the message author is not the bot, and the message content is "+recon", then strip the message
    content of the "+recon" and save the rest as a variable, open a file called "out.txt" and truncate
    it, send a message to the channel saying "Scanning Started on : " and the variable, run the
    subfinder command and save the output as a variable, send a message to the channel saying "Your
    result:- \n", and send the file "out.txt" to the channel
    
    :param message: The message object that triggered the event
    :return: The output of the command is being returned.
    """
    if message.author == client.user:
        return

    msg=message.content
    if '+recon' in msg:
        url = str.strip(msg.split("+recon",1)[1])
        # Opening the file "out.txt" in read and write mode, seeking to the beginning of the file, and
        # truncating the file.
        f = open("out.txt", "r+")
        f.seek(0)
        f.truncate()
        await message.channel.send("Scanning Started on : "+url)
        stream = os.popen("subfinder -d "+url+" -silent -o out.txt")
        output = stream.read()
        await message.channel.send("Your result:- \n")
        await message.channel.send(file=discord.File("out.txt"))

    elif '+scan' in msg:
        ip = str.strip(msg.split("+scan",1)[1])
        # Opening the file "out.txt" in read and write mode, seeking to the beginning of the file, and
        # truncating the file.
        await message.channel.send("Scanning Started on : "+ip)
        #stream = subprocess.run(["rustscan", "-a", "+ip+", "port_scan.txt" ])
        stream = os.popen("rustscan -a "+ip+" > port_scan.txt")
        output = stream.read()
        await message.channel.send("Your result:- \n")
        await message.channel.send(file=discord.File("port_scan.txt"))
    else:
        await message.channel.send("Wrong command")

client.run(TOKEN)
