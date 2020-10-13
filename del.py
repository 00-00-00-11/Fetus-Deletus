import discord
import logging
import asyncio
import json
import sys, os
from os import system
import time
from colored import fg, bg, attr
import re
import requests

os.system('cls' if os.name == 'nt' else 'clear')

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    running_mode = 'Frozen/executable'
else:
    try:
        app_full_path = os.path.realpath(__file__)
        application_path = os.path.dirname(app_full_path)
        running_mode = "Non-interactive (e.g. 'python myapp.py')"
    except NameError:
        application_path = os.getcwd()
        running_mode = 'Interactive'

green = fg('#4EC98F')
magenta = fg('#7D0068')
yellow = fg('#FFCC00')
red = fg('#FF0000')
BOLD = attr('bold')
res = attr('reset')

ignoreChannelCount = 0
isBusy = False

version_num = 'v2.0.3'
print(f'\33]0;Fetus Deletus ' + version_num + ' - Developed by: Notorious\a', end='', flush=True)

print(green
+ '  █████▒▓█████▄▄▄█████▓ █    ██   ██████    ▓█████▄ ▓█████  ██▓    ▓█████▄▄▄█████▓ █    ██   ██████ \n'
+ '▓██   ▒ ▓█   ▀▓  ██▒ ▓▒ ██  ▓██▒▒██    ▒    ▒██▀ ██▌▓█   ▀ ▓██▒    ▓█   ▀▓  ██▒ ▓▒ ██  ▓██▒▒██    ▒ \n'
+ '▒████ ░ ▒███  ▒ ▓██░ ▒░▓██  ▒██░░ ▓██▄      ░██   █▌▒███   ▒██░    ▒███  ▒ ▓██░ ▒░▓██  ▒██░░ ▓██▄   \n'
+ '░▓█▒  ░ ▒▓█  ▄░ ▓██▓ ░ ▓▓█  ░██░  ▒   ██▒   ░▓█▄   ▌▒▓█  ▄ ▒██░    ▒▓█  ▄░ ▓██▓ ░ ▓▓█  ░██░  ▒   ██▒\n'
+ '░▒█░    ░▒████▒ ▒██▒ ░ ▒▒█████▓ ▒██████▒▒   ░▒████▓ ░▒████▒░██████▒░▒████▒ ▒██▒ ░ ▒▒█████▓ ▒██████▒▒\n'
+ ' ▒ ░    ░░ ▒░ ░ ▒ ░░   ░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░    ▒▒▓  ▒ ░░ ▒░ ░░ ▒░▓  ░░░ ▒░ ░ ▒ ░░   ░▒▓▒ ▒ ▒ ▒' + yellow + BOLD + version_num + res + green + ' ░\n'
+ ' ░       ░ ░  ░   ░    ░░▒░ ░ ░ ░ ░▒  ░ ░    ░ ▒  ▒  ░ ░  ░░ ░ ▒  ░ ░ ░  ░   ░    ░░▒░ ░ ░ ░ ░▒  ░ ░\n'
+ ' ░ ░       ░    ░       ░░░ ░ ░ ░  ░  ░      ░ ░  ░    ░     ░ ░      ░    ░       ░░░ ░ ░ ░  ░  ░  \n'
+ '           ░  ░           ░           ░        ░       ░  ░    ░  ░   ░  ░           ░           ░  \n'
+ res)

if os.name == 'nt':
    jfile = application_path + '\\settings.json'
    ifile = application_path + '\\ignore_channels.txt'
    igfile = application_path + '\\ignore_guilds.txt'
else:
    jfile = application_path + '/settings.json'
    ifile = application_path + '/ignore_channels.txt'
    igfile = application_path + '/ignore_guilds.txt'

if os.path.exists(jfile):
    jdata = json.load(open(jfile))
else:
    jdata = open(jfile, 'w')
    jtmp = '{\n\"token\":\"Token_Here\",\n\"command_prefix\":\".\",\n\"del_command\":\"d\",\n\"del_all_dms_command\":\"dd\",\n\"del_all_servers_command\":\"ds\",\n\"del_all_command\":\"da\",\n\"ignore_add_command\":\"ia\",\n\"ignore_del_command\":\"id\"\n}'
    jdata.write(jtmp)
    jdata.close()
    jdata = json.load(open(jfile))

os.environ["rg"] = str(jdata['token'])
token = str(jdata['token'])

os.environ["rg"] = str(jdata['command_prefix'])
command_prefix = str(jdata['command_prefix'])

os.environ["rg"] = str(jdata['del_command'])
del_command = str(jdata['del_command'])

os.environ["rg"] = str(jdata['del_all_command'])
del_all_command = str(jdata['del_all_command'])

os.environ["rg"] = str(jdata['del_all_servers_command'])
del_all_servers_command = str(jdata['del_all_servers_command'])

os.environ["rg"] = str(jdata['del_all_dms_command'])
del_all_dms_command = str(jdata['del_all_dms_command'])

os.environ["rg"] = str(jdata['ignore_add_command'])
ignore_add_command = str(jdata['ignore_add_command'])

os.environ["rg"] = str(jdata['ignore_del_command'])
ignore_del_command = str(jdata['ignore_del_command'])

r = requests.get('https://raw.githubusercontent.com/noto-rious/Fetus-Deletus/master/version.txt').text
if r != version_num:
    print(red + 'Looks like you may not be running the most current version. Check https://noto.cf/fd for an update!' + res)
    print()

if token == 'Token_Here':
        print (red + 'You haven\'t properly configured the \'settings.json\' file. Please put your Discord token in settings.json using the correct JSON syntax and then run the program again.' + res)
        time.sleep(30)
        sys.exit()

ignoreChannelList = []
ignoreGuildList = []

if os.path.exists(ifile):
    ignoreChannelList = open(ifile).read().split('\n')
else:
    ignoreChannelList = open(ifile, 'w')
    ignoreChannelList.write('')
    ignoreChannelList.close()

if len(ignoreChannelList) != None:
    ignoreChannelCount = len(ignoreChannelList)-1
else:
    ignoreChannelCount = 0

if os.path.exists(igfile):
    ignoreGuildList = open(igfile).read().split('\n')
else:
    ignoreGuildList = open(igfile, 'w')
    ignoreGuildList.write('')
    ignoreGuildList.close()

if len(ignoreGuildList) != None:
    ignoreGuildCount = len(ignoreGuildList)-1
else:
    ignoreGuildCount = 0

ready = False
client = discord.Client()

def printWelcome():
    print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> Welcome, ' + green + BOLD + str(client.user) + res + '.')
    print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> You are ignoring ' + green + BOLD + f'{ignoreChannelCount:,}' + res + ' channel(s) and ' + green + BOLD + str(ignoreGuildCount) + res + ' server(s)')
    print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> Your commands are ' + green + BOLD + command_prefix + del_command + res + ',' + green + BOLD + command_prefix + del_all_dms_command + res + ', ' + green + BOLD + command_prefix + del_all_servers_command + res + ', ' + green + BOLD +  command_prefix + del_all_command + res + ', ' + green + BOLD +  command_prefix + ignore_add_command + res + ' and ' + green + BOLD +  command_prefix + ignore_del_command + res)
    print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> Monitoring ' + green + BOLD + calc_Chan() + res + ' channels in ' + green + BOLD + f'{len(client.guilds):,}' + res + ' servers and ' + green + BOLD + f'{len(client.users):,}' + res + ' DM\'s.')
    print()

def progress(count, total, status=''):
    bar_len = 8
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar =  '='  * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write("\033[K")
    sys.stdout.write('\r[%s %s%s] %s\r' % (green + bar + res, yellow + str(percents), '%' + res, status))
    
    sys.stdout.flush()

def calc_time(start):
    elapsed = time.time() - start
    seconds = elapsed % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60  
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def calc_Chan():
    chans = 0
    for guild in client.guilds:
        chans += len(guild.channels)
    chans += len(client.users)
    chans = chans - len(ignoreChannelList)-1
    return f'{chans:,}'

def ChanID(message):
    if isinstance(message.channel, discord.DMChannel): 
        return message.channel.recipient.id
    elif isinstance(message.channel, discord.GroupChannel):
        return message.channel.id
    elif isinstance(message.channel, discord.TextChannel):
        return message.guild.id

def Chan(message):
    if isinstance(message.channel, discord.DMChannel):
        return 'DM with ' + green + BOLD + format_name(str(message.channel.recipient)) + res
    elif isinstance(message.channel, discord.TextChannel):
        return 'in ' +  green + BOLD +  format_name(str(message.guild)) + res
    elif isinstance(message.channel, discord.GroupChannel):
        return 'Group DM: ' +  green + BOLD +  format_name(str(message.channel)) + res

def format_name(name):
    name = (name[:27] + '...') if len(name) > 30 else name
    return name

@client.event
async def AddGuildIgnore(guild):
    global ignoreGuildList
    if str(guild.id) not in(ignoreGuildList):
        ignoreGuildList.append(str(guild.id))
        with open(igfile, 'a') as f:
            f.write(str(guild.id) + '\n')
            f.close()
        if isBusy != True:
            print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> Added ' + green + BOLD + format_name(str(guild.name)) + res + ' to the server ignore list.')
            print()
    else:
        if isBusy != True:
            print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> ' + red + BOLD + format_name(str(guild.name)) + res + ' is already in the server ignore list.')
            print()

@client.event
async def AddChannelIgnore(channel):
    global ignoreChannelList
    if str(channel.id) not in(ignoreChannelList):
        ignoreChannelList.append(str(channel.id))
        with open(ifile, 'a') as f:
            f.write(str(channel.id) + '\n')
            f.close()
        if isBusy != True:
            print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> Added ' + green + BOLD + format_name(str(channel)) + res + ' to the channel ignore list.')
            print()
    else:
        if isBusy != True:
            print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> ' + red + BOLD + format_name(str(channel)) + res + ' is already in the channel ignore list.')
            print()

@client.event
async def DelGuildIgnore(guild):
    global ignoreGuildList
    if str(guild.id) in(ignoreGuildList):
        ignoreGuildList.remove(str(guild.id))
        with open(igfile, "r") as f:
            lines = f.readlines()
            with open(igfile, "w") as f:
                for line in lines:
                    if line.strip("\n") != str(guild.id):
                        f.write(line)
                    
        ignoreGuildList = open(igfile).read().split('\n')
        if isBusy != True:
            print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> Removed ' + green + BOLD + format_name(str(guild.name)) + res + ' from the server ignore list.')
            print()
    else:
        if isBusy != True:
            print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> ' + red + BOLD + format_name(str(guild.name)) + res + ' is not in the server ignore list.')
            print()

@client.event
async def DelChannelIgnore(channel):
    global ignoreChannelList
    if str(channel.id) in(ignoreChannelList):
        ignoreChannelList.remove(str(channel.id))
        with open(ifile, "r") as f:
            lines = f.readlines()
            with open(ifile, "w") as f:
                for line in lines:
                    if line.strip("\n") != str(channel.id):
                        f.write(line)
                    
        ignoreChannelList = open(ifile).read().split('\n')
        if isBusy != True:
            print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> Removed ' + green + BOLD + format_name(str(channel)) + res + ' from the channel ignore list.')
            print()
    else:
        if isBusy != True:
            print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> ' + red + BOLD + format_name(str(channel)) + res + ' is not in the channel ignore list.')
            print()

@client.event
async def on_connect():
    global ready
    if ready == False:
        ready = True
        printWelcome()

@client.event
async def on_ready():
    global ready
    if ready == False:
        ready = True
        printWelcome()

@client.event
async def on_message(message):
    global ready
    global isBusy
    global ignoreChannelList
    global ignoreGuildList


    if ready == False:
        ready = True
        printWelcome()

    if message.content.startswith(command_prefix + ignore_add_command) and message.author == client.user:
        if isinstance(message.channel, discord.DMChannel): 
            await AddChannelIgnore(message.channel.recipient)
        elif isinstance(message.channel, discord.GroupChannel):
            await AddChannelIgnore(message.channel)
        elif isinstance(message.channel, discord.TextChannel):
            await AddGuildIgnore(message.guild)

        await DeleteCommand(message)

    if message.content.startswith(command_prefix + ignore_del_command) and message.author == client.user and isBusy == False:
        if isinstance(message.channel, discord.DMChannel): 
            await DelChannelIgnore(message.channel.recipient)
        elif isinstance(message.channel, discord.GroupChannel):
            await DelChannelIgnore(message.channel)
        elif isinstance(message.channel, discord.TextChannel):
            await DelGuildIgnore(message.guild)
      
        await DeleteCommand(message)

    if message.content == command_prefix + del_all_command and message.author == client.user:
        if isBusy == True:
            await DeleteCommand(message)
            return

        isBusy = True
        await DeleteCommand(message)
        print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> ' + green + BOLD + command_prefix + del_all_command + res + ' accepted in ' + Chan(message) + res + '. Please wait...')
        await DeleteAll()
        print()
    elif message.content.startswith(command_prefix + del_all_dms_command)  and message.author == client.user:
        if isBusy == True:
            await DeleteCommand(message)
            return

        isBusy = True
        await DeleteCommand(message)
        print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> ' + green + BOLD + command_prefix + del_all_dms_command + res + ' accepted in ' + Chan(message) + res + '. Please wait...')
        await DeleteAllDMs()
        print()
    elif message.content.startswith(command_prefix + del_all_servers_command)  and message.author == client.user:
        if isBusy == True:
            await DeleteCommand(message)
            return

        isBusy = True
        await DeleteCommand(message)
        print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> ' + green + BOLD + command_prefix + del_all_servers_command + res + ' accepted in ' + Chan(message) + res + '. Please wait...')
        await DeleteAllServers()
        print()

    elif message.content.startswith(command_prefix + del_command + ' ')  and message.author == client.user:
        if isBusy == True:
            await DeleteCommand(message)
            return

        if str(ChanID(message)) in(ignoreChannelList) or str(ChanID(message)) in(ignoreGuildList):
            await DeleteCommand(message)
            if str(ChanID(message)) in(ignoreChannelList):
                print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> You can\'t delete messages sent to ' + red + BOLD + str(Chan(message)) + res + '.')
            if str(ChanID(message)) in(ignoreGuildList):
                print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> You can\'t delete messages sent to ' + red + BOLD + format_name(str(message.guild.name)) + res + '.')
        else:
            msg = message.content
            t = msg[len(command_prefix + del_command):].strip()
            t = re.sub('[^0-9]','', t)
            print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> Deleting messages sent to ' + green + BOLD + str(Chan(message)) + res + '. Please wait...')
            await DeleteMessages(message,t)
            print()

    elif message.content == command_prefix + del_command  and message.author == client.user:
        if isBusy == True:
            await DeleteCommand(message)
            return
    
        if str(ChanID(message)) in(ignoreChannelList) or str(ChanID(message)) in(ignoreGuildList):
            await DeleteCommand(message)
            if str(ChanID(message)) in(ignoreChannelList):
                print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> You can\'t delete messages sent to ' + red + BOLD + str(Chan(message)) + res + '.')
            if str(ChanID(message)) in(ignoreGuildList):
                print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> You can\'t delete messages sent to ' + red + BOLD + format_name(str(message.guild.name)) + res + '.')
        else:
            print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> Deleting messages sent to ' + green + BOLD + str(Chan(message)) + res + '. Please wait...')
            await DeleteMessages(message,99999)
            print()

@client.event
async def DeleteAllDMs():
    global ignoreChannelList
    global isBusy
    start_time = time.time()
    i = 0
    counter = 0
    theID = 0
    maxLen = len(client.private_channels)
    for channel in client.private_channels:
        if isinstance(channel, discord.DMChannel): 
            tmp_chan = res + 'DM with ' + green + BOLD + format_name(str(channel.recipient))
            theID = channel.recipient.id
        elif isinstance(channel, discord.GroupChannel):
            tmp_chan =  res + 'Group DM: ' + green + BOLD + format_name(str(channel))
            theID = channel.id
        if str(theID) not in(ignoreChannelList):
            async for message in channel.history(limit=None):
                try:
                    if message.author == client.user:
                        await message.delete()
                        counter += 1
                except Exception as e:
                        pass
                progress(i, maxLen, status='Deleted ' + green + BOLD + f'{counter:,}'  + res + ' sent Messages.' + res + ' - Elapsed: ' + green + BOLD + calc_time(start_time) + res + ' - in ' + green + BOLD + tmp_chan + res)
        i += 1

    progress(maxLen, maxLen, status=' FINISHED! Elapsed Time: ' + green + BOLD + calc_time(start_time) + res + ' - Total Deleted: ' + green + BOLD + f'{counter:,}' + res)
    print()
    isBusy = False

@client.event
async def DeleteAllServers():
    global ignoreChannelList
    global isBusy
    start_time = time.time()
    i = 0
    counter = 0
    maxLen = len(client.guilds)
    for guild in client.guilds:
        if str(guild.id) not in(ignoreGuildList):
            for channel in guild.text_channels:
                try:
                    async for message in channel.history(limit=None):
                        if message.author == client.user:
                            await message.delete()
                            counter += 1
                        progress(i, maxLen, status='Deleted ' + green + BOLD + f'{counter:,}'  + res + ' sent Messages.' + res + ' - Elapsed: ' + green + BOLD + calc_time(start_time) + res + ' - in ' + green + BOLD + format_name(str(guild)) + res)
                except Exception as e:
                    pass
        i += 1

    progress(i, maxLen, status=' FINISHED! Elapsed Time: ' + green + BOLD + calc_time(start_time) + res + ' - Total Deleted: ' + green + BOLD + f'{counter:,}' + res)
    print()
    isBusy = False

@client.event
async def DeleteAll():
    global ignoreChannelList
    global isBusy
    start_time = time.time()
    i = 0
    counter = 0
    theID = 0
    maxLen = len(client.private_channels) + len(client.guilds)
    for channel in client.private_channels:
        if isinstance(channel, discord.DMChannel): 
            tmp_chan = res + 'DM with ' + green + BOLD + format_name(str(channel.recipient))
            theID = channel.recipient.id
        elif isinstance(channel, discord.GroupChannel):
            tmp_chan =  res + 'Group DM: ' + green + BOLD + format_name(str(channel))
            theID = channel.id
        if str(theID) not in(ignoreChannelList):
            async for message in channel.history(limit=None):
                try:
                    if message.author == client.user:
                        await message.delete()
                        counter += 1
                except Exception as e:
                        pass
                progress(i, maxLen, status='Deleted ' + green + BOLD + f'{counter:,}'  + res + ' sent Messages.' + res + ' - Elapsed: ' + green + BOLD + calc_time(start_time) + res + ' - in ' + green + BOLD + tmp_chan + res)
        i += 1
    if i == maxLen:
        progress(i, maxLen, status=' FINISHED! Elapsed Time: ' + green + BOLD + calc_time(start_time) + res + ' - Total Deleted: ' + green + BOLD + f'{counter:,}' + res)
        print()

    for guild in client.guilds:
        if str(guild.id) not in(ignoreGuildList):
            for channel in guild.text_channels:
                try:
                    async for message in channel.history(limit=None):
                        if message.author == client.user:
                            await message.delete()
                            counter += 1
                        progress(i, maxLen, status='Deleted ' + green + BOLD + f'{counter:,}'  + res + ' sent Messages.' + res + ' - Elapsed: ' + green + BOLD + calc_time(start_time) + res + ' - in ' + green + BOLD + format_name(str(guild)) + res)
                except Exception as e:
                    pass
        i += 1

    progress(i, maxLen, status=' FINISHED! Elapsed Time: ' + green + BOLD + calc_time(start_time) + res + ' - Total Deleted: ' + green + BOLD + f'{counter:,}' + res)
    print()
    isBusy = False

@client.event
async def DeleteMessages(message,max):
    counter = 0
    async for msg in message.channel.history(limit=None):
        if  int(max) > counter:
            try:
                if msg.author == client.user:
                    await msg.delete()
                    counter += 1
            except Exception as e:
                pass
        else:
            pass
    print(res + magenta + time.strftime('%I:%M %p', time.localtime()).rstrip() + res + ' -> Fetus Deletus -> Finished deleting ' + green + BOLD + str(counter) + res + ' messages sent to ' + str(Chan(message)) + res + '.')


@client.event
async def DeleteCommand(message):
    await message.edit(content='x')
    await message.edit(content='xD')
    await message.delete()

client.run(token, bot=False)