import discord, asyncio, os, boto3

client = discord.Client()

ec2 = boto3.resource('ec2')
#Temp
instance = ec2.Instance('i-06bc2e80c17a5636c')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')

@client.event
async def on_message(message):
    memberIDs = (member.id for member in message.mentions)
    if client.user.id in memberIDs:
        if 'stop' in message.content:
            if turnOffInstance():
                await message.channel.send('AWS Instance stopping')
            else:
                await message.channel.send('Error stopping AWS Instance')
        elif 'start' in message.content:
            if turnOnInstance():
                await message.channel.send('AWS Instance starting')
            else:
                await message.channel.send('Error starting AWS Instance')
        elif 'state' in message.content:
            await message.channel.send('AWS Instance state is: ' + getInstanceState())
        elif 'reboot' in message.content:
            if rebootInstance():
                await message.channel.send('AWS Instance rebooting')
            else:
                await message.channel.send('Error rebooting AWS Instance')

def turnOffInstance():
    try:
        instance.stop(False, False, True)
        return True
    except:
        return False

def turnOnInstance():
    try:
        instance.start()
        return True
    except:
        return False

def getInstanceState():
    return instance.state['Name']

def rebootInstance():
    try:
        instance.reboot()
        return True
    except:
        return False


client.run(os.environ['AWSDISCORDTOKEN'])
