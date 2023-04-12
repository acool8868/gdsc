import os
import openai
import discord
import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = "MTA5NTMyMjM5OTc3NzUwNTMyMQ.GqWWsK.qa30dsmlidrdvVEcX0iEKSnPBSrWTerFX9a8eM"
openai.api_key = os.getenv('OPENAI_KEY')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    print(message)

    if user_message.lower() == "gpt":
        await message.channel.send("chat")
        return
    elif user_message.split(' ')[0].lower() == "rem":
        print("time")
    elif user_message.split(' ')[0].lower() == "song":
        print("music")

client.run(TOKEN)

'''def get_response(prompt):
    model_engine = "text-davinci-002"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()'''

