import discord, asyncio, os, boto3

client = discord.Client()

ec2 = boto3.resource('ec2')
#Temp
instance = ec2.Instance('')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')

@client.event
async def on_message(message):
    drugs = ["shabu","drugs","juts","marijuana","cocaine","meth"]
    memberIDs = (member.id for member in message.mentions)
    if client.user.id in memberIDs:
        if 'pa-stop' in message.content:
            if turnOffInstance():
                await message.channel.send('Ayan stopping na.')
            else:
                await message.channel.send('Sira pa eh, ipagapatawad mo.')
        elif 'pa-start' in message.content:
            if turnOnInstance():
                await message.channel.send('Ayan starting na.')
            else:
                await message.channel.send('Ayaw')
        elif 'musta' in message.content:
            await message.channel.send('Dabarkads, ang server ay kasalukuyang ' + getInstanceState())
        elif 'pa-reboot' in message.content:
            if rebootInstance():
                await message.channel.send('off-on ko lang saglit')
            else:
                await message.channel.send('Ayaw')
        elif 'kanta ka nga' in message.content:
            await message.channel.send('Paos pa ko dabarkads, saka na lang.')

    if any(a in message.content for a in drugs):
        await message.reply("Nako bawal yan dabarkads")

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
