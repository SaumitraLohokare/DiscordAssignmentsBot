import lms_vitcc
import os
import json
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

client = discord.Client()

JSON_FILE = 'user_data.json'
USER_DETAILS = {}

async def get_user_details(message):
    global USER_DETAILS
    await message.author.create_dm()
    if USER_DETAILS.get(str(message.author)) == None:
        args = message.content.split(' ')
        try:
            username, password = args[1:]
        except Exception:
            await message.author.dm_channel.send('Incorrect format.')
            return
        USER_DETAILS[str(message.author)] = { username: password }
        print('Added new user.')
        with open(JSON_FILE) as f:
            feeds = json.load(f)
        feeds[str(message.author)] = { username: password }
        with open(JSON_FILE, mode='w') as f:
            f.write(json.dumps(feeds))
        await message.author.dm_channel.send('Detials stored!')
    else:
        await message.author.dm_channel.send('Your details are already recorded!')

def load_users():
    global USER_DETAILS
    with open(JSON_FILE) as f:
        USER_DETAILS = json.load(f)
        print('loaded users:')
        print(USER_DETAILS)

async def setup_user(user):
    await user.create_dm()
    await user.dm_channel.send('Enter your lms username and password in the following format:\n`.details username password`')

async def check_assignments(user):
    global USER_DETAILS
    await user.create_dm()
    await user.dm_channel.send('Retrieving your assignments...')
    if USER_DETAILS.get(str(user)) != None:
        username, password = list(USER_DETAILS.get(str(user)).items())[0]
    else:
        await user.dm_channel.send('Your details are not recorded... \nUse `.setup`')
        return
    assignments = await lms_vitcc.getAssignments(username, password)
    await user.dm_channel.send(assignments)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('.'):
        args = message.content.split(' ')
        if args[0] == '.setup':
            await setup_user(message.author)
        elif args[0] == '.check':
            await check_assignments(message.author)
        elif args[0] == '.details':
            await get_user_details(message)

def main():
    load_users()
    client.run(TOKEN)

if __name__ == '__main__':
    main()