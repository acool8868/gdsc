import os
import openai
import discord
import datetime
import asyncio
from dotenv import load_dotenv

reminder_mess = ""
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv('OPENAI_KEY')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

async def schedule_reminder(reminder_time, message1, message):
    now = datetime.datetime.now()
    delta = (reminder_time - now).total_seconds()
    await asyncio.sleep(delta)
    await message.channel.send("Reminder: It's now " + str(reminder_time)+"\n"+ str(' '.join(message1)))
@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
    if user_message.split(' ')[0].lower() == "help":
        await message.channel.send("1. \'gpt\' + prompt\n2. \'rem\' + mm:hh::dd/mm/yyyy + message\n3. \'song\' + name")
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
        try:
            reminder_time = datetime.datetime.strptime(user_message.split(' ')[1], '%H:%M::%d/%m/%Y')
            reminder_mess = user_message.split(' ')[2::]
            await message.channel.send("Reminder set for " + str(reminder_time))
            await schedule_reminder(reminder_time, reminder_mess, message)
        except ValueError:
            await message.channel.send("Invalid reminder format. Please use the format \'rem HH:MM::DD/MM/YYYY (message)\'")
        return
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




