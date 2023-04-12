import os
import openai
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv('OPENAI_KEY')
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} is connected to the following guild:')

client.run(TOKEN)