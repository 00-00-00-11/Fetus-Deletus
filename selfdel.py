import discord
import logging
import asyncio
import json
import sys, os
from os import system
import time
import colorama
from colorama import Fore, Back, Style, init
import re
import requests

init()
app_version = 'v1.0.25'

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

if os == 'Windows':
    system('cls')
    jfile = application_path + '\\config.json'
    wfile = application_path + '\\whitelist.txt'
else:
    system('clear')
    print(chr(27) + '[2J')
    jfile = application_path + '/config.json'
    wfile = application_path + '/whitelist.txt'


if os.path.exists(jfile):
    jdata = json.load(open(jfile))
else:
    jdata = open(jfile, 'w')
    jdata.write('{\"token\":\"Token_Here\",\"cleanphrase\":\"?del\",\"cleanallphrase\":\"?all\",\"whitelistaddphrase\":\"?wa\",\"whitelistdelphrase\":\"?wd\"}')
    jdata.close()
    jdata = json.load(open(jfile))
if os.path.exists(wfile):
    wlines = open(wfile).read().split('\n')
else:
    wlines = open(wfile, 'w')
    wlines.write('')
    wlines.close()
    wlines = open(wfile).read().split('\n')

#system('title Fetus Deletus ' + app_version + ' - Developed by: Notorious') internally deprecated in 1.0.24
print(f'\33]0;Fetus Deletus ' + app_version + ' - Developed by: Notorious\a', end='', flush=True)
#ctypes.windll.kernel32.SetConsoleTitleW('Fetus Deletus ' + app_version + ' - Developed by: Notorious') internally deprecated in 1.0.15

print(Fore.GREEN + " ███████╗███████╗████████╗██╗   ██╗███████╗    ██████╗ ███████╗██╗     ███████╗████████╗██╗   ██╗███████╗")
print(" ██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔════╝    ██╔══██╗██╔════╝██║     ██╔════╝╚══██╔══╝██║   ██║██╔════╝")
print(" █████╗  █████╗     ██║   ██║   ██║███████╗    ██║  ██║█████╗  ██║     █████╗     ██║   ██║   ██║███████╗")
print(" ██╔══╝  ██╔══╝     ██║   ██║   ██║╚════██║    ██║  ██║██╔══╝  ██║     ██╔══╝     ██║   ██║   ██║╚════██║")
print(" ██║     ███████╗   ██║   ╚██████╔╝███████║    ██████╔╝███████╗███████╗███████╗   ██║   ╚██████╔╝███████║")
print(" ╚═╝     ╚══════╝   ╚═╝    ╚═════╝ ╚══════╝    ╚═════╝ ╚══════╝╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚══════╝ " + app_version + "\n" + Fore.RESET)

vlink = 'https://noto.cf/fd_ver.txt'
f = requests.get(vlink)
if f.text != app_version:
    print(Fore.LIGHTRED_EX + 'Looks like you may not be running the most current version. Check https://noto.cf/ for an update.\n' + Fore.RESET)

client = discord.Client()
os.environ["rg"] = str(jdata['token'])
token = str(jdata['token'])
cleanphrase = str(jdata["cleanphrase"]).strip()
cleanallphrase = str(jdata["cleanallphrase"]).strip()
wlaphrase = str(jdata["whitelistaddphrase"]).strip()
wldphrase = str(jdata["whitelistdelphrase"]).strip()

wlength = len(wlines)-1
print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + Fore.RESET + '] - White-list Users Loaded: ' + Fore.MAGENTA + str(f"{wlength:,d}") + Fore.RESET + '\n')

if token == "Token_Here":
        print ("You haven't properly configured the \'config.json\' file. Please put your Discord token in config.json using the correct JSON syntax and then run the program again.")
        time.sleep(8)
        sys.exit()

print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + Fore.RESET + '] - Now listening for ' + Fore.YELLOW + cleanphrase + Fore.RESET + Fore.GREEN + ' (+ x)' + Fore.RESET + ', ' + Fore.YELLOW + cleanallphrase + Fore.RESET + ', ' + Fore.YELLOW + wlaphrase + Fore.RESET + ' or ' + Fore.YELLOW + wldphrase + Fore.RESET + ' in all Discord channels.')

@client.event
async def on_message(message):
    counter = 0
    counter2 = 0
    skipped = 0
    if message.channel.type is discord.ChannelType.group:
        chanid = str(message.channel.id)
        channame = str(message.channel.name)
    elif message.channel.type is discord.ChannelType.private:
        chanid = str(message.channel.recipient.id)
        channame = str(message.channel.recipient.name)
    else:
        chanid = str(message.guild.id)
        channame = str(message.guild.name)

    if message.content.startswith(str(cleanphrase)) and message.author == client.user:
        await message.delete()
        if re.search(r'[^\S\n\t]+', message.content) is not None:
            t = message.content[len(cleanphrase):].strip()
            t = re.sub(r'[`!@#$%^&*()_+=-~ ?/\\.,;{}qwertyuiopasdfghjklzxcvbnm\']', '', t)
            t = int(t)
            throttled = 'True'
            print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p',
                                                          time.localtime()).rstrip() + Fore.RESET + '] - Delete phrase: ' + Fore.YELLOW + cleanphrase + Fore.RESET + ' ' + Fore.GREEN + str(f"{t:,d}") + Fore.RESET + ' has been accepted in: ' + Fore.MAGENTA + channame.rstrip() + Fore.RESET + '. Processing...')
        else:
            throttled = 'False'
            t = 9999999
            print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p',
                                                          time.localtime()).rstrip() + Fore.RESET + '] - Delete phrase: ' + Fore.YELLOW + cleanphrase + Fore.RESET + ' has been accepted in: ' + Fore.MAGENTA + channame.rstrip() + Fore.RESET + '. Processing...')

        async for message in message.channel.history(limit=9999999):
            if message.author == client.user and str(message.type) == 'MessageType.default':
                if throttled == 'True' and t > counter:
                    await message.delete()
                    counter += 1
                    print(f'\33]0;Fetus Deletus ' + app_version + ' - Deleted: ' + str(f"{counter:,d}") + ' messages.\a', end='', flush=True)
                elif throttled == 'False':
                    await message.delete()
                    counter += 1
                    print(f'\33]0;Fetus Deletus ' + app_version + ' - Deleted: ' + str(f"{counter:,d}") + ' messages.\a', end='', flush=True)
        msg = "✅`Cleaned " + str(f"{counter:,d}") + " messages.`"
        end = await message.channel.send(msg)
        print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p',
                                                      time.localtime()).rstrip() + Fore.RESET + '] - Finished deleting ' + Fore.GREEN + str(f"{counter:,d}") + Fore.RESET + ' messages in ' + Fore.MAGENTA + channame.rstrip() + Fore.RESET + '.')
        print(f'\33]0;Fetus Deletus ' + app_version + ' - Developed by: Notorious\a', end='', flush=True)
        await asyncio.sleep(3)
        await end.delete()
    if message.content.startswith(str(cleanallphrase)) and message.author == client.user:
            wlines = open(wfile).read().split('\n')
            wlength = len(wlines)-1
            await message.delete()
            print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p', time.localtime()).rstrip() + Fore.RESET + '] - Delete phrase: ' + Fore.YELLOW + cleanallphrase + Fore.RESET + ' has been accepted in: ' + Fore.MAGENTA + channame + Fore.RESET + '. Deleting Outbound DM\'s...')
            for channel in client.private_channels:
                if message.channel.type is discord.ChannelType.private or discord.ChannelType.text or discord.ChannelType.group:
                 async for message in channel.history(limit=99999):
                    try:
                        counter2 += 1
                        chanid = str(message.channel.recipient.id)
                        if message.author == client.user and chanid not in(wlines):
                            await message.delete()
                            counter += 1
                            print(f'\33]0;Fetus Deletus ' + app_version + ' - Deleted: ' + str(f"{counter:,d}") + ' messages.\a', end='', flush=True)
                        elif chanid in(wlines):
                            skipped += 1

                    except:
                     pass

            print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p ',
                                                          time.localtime()).rstrip() + Fore.RESET + '] - Finished deleting ' + Fore.GREEN + str(f"{counter:,d}") + Fore.RESET + ' and skipped ' + Fore.LIGHTRED_EX + str(f"{skipped:,d}") + Fore.RESET + ' out of ' + Fore.MAGENTA + str(f"{counter2:,d}") + Fore.RESET + '.')
            print(f'\33]0;Fetus Deletus ' + app_version + ' - Developed by: Notorious\a', end='', flush=True)

    if message.content.startswith(str(wlaphrase)) and message.author == client.user:
        errored = 0
        await message.delete()
        if message.content.startswith(str(wlaphrase) + ' ') and "@" in message.content:
            who_to_wl = message.content.split('<@!')[1]
            who_to_wl = who_to_wl.split('>')[0]
        elif message.content.startswith(str(wlaphrase) + ' '):
            who_to_wl = message.content.split(' ')[1]
        elif message.channel.type is discord.ChannelType.private:
            who_to_wl = message.channel.recipient.id
        else:
            print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p ',
                                                          time.localtime()).rstrip() + Fore.RESET + '] - White-List phrase: ' + Fore.LIGHTRED_EX + wlaphrase + Fore.RESET + ' syntax not recognized.')
            errored = 1
        if errored != 1:
            wlines = open(wfile).read().split('\n')
            wlength = len(wlines)-1

            if str(who_to_wl) not in(wlines):
                f = open(wfile, 'a')
                f.write(str(who_to_wl) + '\n')
                f.close()
                wlines = open(wfile).read().split('\n')
                wlength = len(wlines)-1
                print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p',
                                                              time.localtime()).rstrip() + Fore.RESET + '] - User ID: ' + Fore.GREEN + str(who_to_wl) + Fore.RESET + ' has been added to the White-List! Users Loaded: ' + Fore.MAGENTA + str(f"{wlength:,d}") + Fore.RESET)
            else:
                print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p',
                                                              time.localtime()).rstrip() + Fore.RESET + '] - User ID: ' + Fore.LIGHTRED_EX + str(who_to_wl) + Fore.RESET + ' already exists in the White-List!')

    if message.content.startswith(str(wldphrase)) and message.author == client.user:
        errored = 0
        await message.delete()
        if message.content.startswith(str(wldphrase) + ' ') and "@" in message.content:
            who_to_wl = message.content.split('<@!')[1]
            who_to_wl = who_to_wl.split('>')[0]
        elif message.content.startswith(str(wldphrase) + ' '):
            who_to_wl = message.content.split(' ')[1]
        elif message.channel.type is discord.ChannelType.private:
            who_to_wl = message.channel.recipient.id
        else:
            print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p ',
                                                          time.localtime()).rstrip() + Fore.RESET + '] - White-List phrase: ' + Fore.LIGHTRED_EX + wldphrase + Fore.RESET + ' syntax not recognized.')
            errored = 1
        if errored != 1:
            wlines = open(wfile).read().split('\n')
            wlength = len(wlines)-1

            if str(who_to_wl) in (wlines):
                with open(wfile, "r") as f:
                    lines = f.readlines()
                with open(wfile, "w") as f:
                    for line in lines:
                        if line.strip("\n") != str(who_to_wl):
                            f.write(line)

                wlines = open(wfile).read().split('\n')
                wlength = len(wlines)-1
                print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p',
                                                                    time.localtime()).rstrip() + Fore.RESET + '] - User ID: ' + Fore.LIGHTRED_EX + str(who_to_wl) + Fore.RESET + ' has been removed from the White-List! Users Loaded: ' + Fore.MAGENTA + str(f"{wlength:,d}") + Fore.RESET)
            else:
                print('[' + Fore.LIGHTBLUE_EX + time.strftime('%I:%M:%S %p',
                                                                    time.localtime()).rstrip() + Fore.RESET + '] - User ID: ' + Fore.LIGHTRED_EX + str(who_to_wl) + Fore.RESET + ' not found in the White-List!')
client.run(token, bot=False)
