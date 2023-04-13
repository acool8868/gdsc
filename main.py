import os
import openai
import discord
import datetime
import asyncio
from dotenv import load_dotenv

timers = []
reminder_mess = ""
timer_counter = 0
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv('OPENAI_KEY')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

async def schedule_reminder(reminder_time, message1, message, count_t):
    global timers

    timers.append([reminder_time, message1, count_t])
    now = datetime.datetime.now()
    delta = (timers[0][0] - now).total_seconds()
    await asyncio.sleep(delta)
    await message.channel.send("Reminder " + timers[0][2] + ": It's now " + str(timers[0][0])+"\n"+ str(' '.join(timers[0][1])))


@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
    global timer_counter
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
            timer_counter += 1
            await schedule_reminder(reminder_time, reminder_mess, message, timer_counter)
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




