import os
import openai
import discord
import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv('OPENAI_KEY')

intents = discord.Intents.all()

client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
    if user_message.split(' ')[0].lower() == "help":
        await message.channel.send("1. \'gpt\' + prompt\n2. \'rem\' + mm:hh (24 hour time) dd/mm/yyyy\n3. \'song\' + name")
        return
    elif user_message.split(' ')[0].lower() == "gpt":
        await message.channel.send("[imagine chatgpt's reply here]")
        superprompt = "You are a bot on discord, you must reply " \
                      "is a short and precise manner. Only do as " \
                      "you are told. You can add discord formatting" \
                      ". I am " + username + "The prompt is :" + user_message
        await message.channel.send(get_response(superprompt))
        return
    elif user_message.split(' ')[0].lower() == "rem":

    elif user_message.split(' ')[0].lower() == "song":
        print("music")

client.run(TOKEN)

def get_response(prompt):
    model_engine = "text-davinci-002"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return str(response.choices[0].text.strip())


