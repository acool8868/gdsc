# gdsc
gdsc_projects


README file for Discord Bot with Chatgpt access and Reminders

INTRODUCTION\
This project is a Discord bot built in Python that has chat and reminder functionality. The bot uses the OpenAI GPT-3 API to respond to user messages and allows users to create, delete, and modify reminders by sending a message with the time and date of the reminder in a specific format.


INSTALLATION AND SETUP\
Discord.py: A Python library for creating Discord bots\
OpenAI: A Python library for interacting with the OpenAI GPT-3 API\
Dotenv: A Python library for loading environment variables from a .env file\
Once you have installed these packages, clone the repository to your local machine and create a .env file in the root directory of the project. In the .env file, add your Discord bot token and OpenAI API key in the following format:
DISCORD_TOKEN=your_discord_token_here
OPENAI_KEY=your_openai_key_here


USAGE COMMANDS:
1. 'gpt' + prompt
2. 'remnew' + time (mm:hh::dd/mm/yyyy) + message
3. 'remedit' + serial number + new time (same format)
4. 'remdel' + serial number
5. 'song' + action(play, pause, queue, next) + name
