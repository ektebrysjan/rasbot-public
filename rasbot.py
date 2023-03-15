# Link for token: https://discordapp.com/oauth2/authorize?client_id= ***CLIENTID*** &scope=bot&permissions=8

import asyncio
from discord.ext import commands
import discord as discord
import random
import json
import openai

# Put your API token here
openai.api_key = ""

startPrompt = []
conversation = []
summary = ". "

# System prompt which inserts the name of the user and previous conversation topics to simulate actual long term memory.
def itBot(userN="Brethren"):
    global startPrompt
    global summary
    print("Initializing conversation history")
    startPrompt = [{"role": "system", "content" : f"You are a Jamaican man named Liam who responds in Patois. Randomly end sentences with phrases like Safe, Bless, Big up, Bless Up, Irie, Yahso. Avoid calling yourself a bot or an assistant. Recent topics include: {summary}. The following user is named {userN}"}]
    return startPrompt
itBot()

intents = discord.Intents.all()

# Get config from json file
f = open("config.json", "r")
config = f.read()


config = json.loads(config)

# For loop sets the json values as variables
for setting, v in config.items():
    globals()[setting] = str(v)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    global n, e, u

# Function to summarize conversation for storage, essentially compressing memory to save API tokens
def summarizer(convo):
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=convo,
            max_tokens=300,
            temperature=0,
    )
    summ = response['choices'][0]['message']['content']
    
    print(summ)
    return summ

# Logic for talking with the chatbot
@bot.command()
async def q(ctx, *, arg ="hello"):
    global startPrompt
    global conversation
    global summary
    rol = ctx.author.roles
    user = ctx.author.id    
    channel = ctx.channel.name

    print(user, channel)
    
    # To make sure people do not spend all my token money, limit usage to people in "botasker" discord role
    if "botasker" not in str(rol):
        await ctx.send("Shut up, pencil dick")

     # Insert the previous history for context, then the question, and add "respond in patois" to make sure  the bot stays in character.
    else:
        conversation.append({"role": "user", "content": arg + ". respond in patois."})
        quer = itBot(ctx.author.name) + conversation

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=quer,
        max_tokens=1000,
        temperature=0.9,
        )
       
        resp = response['choices'][0]['message']['content']
        await ctx.send(resp)
        conversation.append({"role": "assistant", "content": resp}
                            
    # If the message log is longer than 4 messages, summarize and clear list to save tokens.
        if len(conversation) > 4:
            convo = conversation
            convo.append({"role": "user", "content" : "please summarize our conversation in as few words as possible and never mention patois!"})
            summary = summary + summarizer(convo)
            conversation = []

bot.run(dctoken)
