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


async def schedule_reminder(message):
    global timers
    print(timers)
    while timers != []:
        now = datetime.datetime.now()
        delta = (timers[0][0] - now).total_seconds()
        print(timers)
        await asyncio.sleep(delta)
        await message.channel.send("Reminder " + str(timers[0][3]) + ": It's now " + str(timers[0][0])+"\n"+ str(' '.join(timers[0][1])))
        timers.pop(0)


@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
    global timer_counter
    global timers
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
    messlist = user_message.split(' ')
    if messlist[0].lower() == "help":
        await message.channel.send("1. \'gpt\' + prompt\n2. \'remnew\' + time (mm:hh::dd/mm/yyyy) + "
                                   "message\n3. \'remedit\' + serial number + new time (same format)"
                                   "\n4. \'remdel\' + serial number\n5. \'song\' + "
                                   "action(play, pause, queue, next) + name")
        return
    elif messlist[0].lower() == "gpt":
        await message.channel.send("[imagine chatgpt's reply here]")
        superprompt = "You are a bot on discord, you must reply " \
                      "is a short and precise manner. Only do as " \
                      "you are told. You can add discord formatting" \
                      ". I am " + username + "The prompt is :" + user_message
        await message.channel.send(get_response(superprompt))
        return
    elif messlist[0].lower() == "remnew":
        try:
            reminder_time = datetime.datetime.strptime(messlist[1], '%H:%M::%d/%m/%Y')
            reminder_mess = messlist[2::]
            timer_counter += 1
            await message.channel.send("Reminder (number " + str(timer_counter)+") set for " + str(reminder_time))
            if len(timers) != 0:
                for i in range(len(timers)):
                    if not timers[i][0] < reminder_time:
                        timers.insert(i, [reminder_time, reminder_mess, message, timer_counter])
                    else:
                        timers.append([reminder_time, reminder_mess, message, timer_counter])
            else:
                timers.append([reminder_time, reminder_mess, message, timer_counter])
            print(timers)
            if len(timers)==1:
                await schedule_reminder(message)
        except ValueError:
            await message.channel.send("Invalid reminder format. Please use the "
                                       "format \'rem HH:MM::DD/MM/YYYY (message)\'")
        return
    elif messlist[0].lower() == "remedit":
        for i in range(len(timers)):
            if str(timers[i][3]) == messlist[1]:
                timers[i][0] = datetime.datetime.strptime(messlist[2], '%H:%M::%d/%m/%Y')
                temptimer = timers[i]
                timers.pop(i)
                for j in range(len(timers)):
                    if not timers[j][0] < temptimer[0]:
                        timers.insert(j, temptimer)
                        print(timers)
                        return
                    else:
                        timers.append(temptimer)
                        print(timers)
                        return
    elif messlist[0].lower() == "remdel":
        for i in range(len(timers)):
            if str(timers[i][3]) == messlist[1]:
                timers.pop(i)
                print(timers)
                return
    elif messlist[0].lower() == "song":
        print("music")
        return

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


