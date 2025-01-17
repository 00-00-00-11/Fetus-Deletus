# Fetus Deletus v2
Fetus Deletus is a Discord.py self-message deleter.  
Version 2 has been completely recoded from scratch in Python 3.8

[![GitHub release](https://img.shields.io/github/v/release/noto-rious/Fetus-Deletus?style=plastic)](https://github.com/noto-rious/Fetus-Deletus/releases) ![GitHub All Releases](https://img.shields.io/github/downloads/noto-rious/Fetus-Deletus/total?style=plastic)

### Features 
* Cross-platform support for Windows and Linux
* Has features that allow you to Delete all sent messages Groups, Servers, or a DM.
* Supports numerical variables (i.e: .d 20 deletes 20 most recent messages)
* Has an ignore list for both Servers and DM's

![](screenshot.png)

### Settings
Edit `settings.json`
```
{
"token":"Token_Here",               //put your discord authorization token here(see instructions on how to obtain down below)
"command_prefix":".",               //this is the command prefix, the character before each command that will be used.
"del_command":"d",                  //this command deletes all or a custom numerical variable(i.e. .d 2) sent messages in current channel.
"del_all_dms_command":"dd",         //this command deletes all sent dm messages for all users.
"del_all_servers_command":"ds",     //this command deletes all sent server messages for all servers.
"del_all_command":"da",             //this command deletes all sent dm and server messages for all users and all servers.
"ignore_add_command":"ia",          //type this command in the channel of the dm/guild you would like to ignore the channel.
"ignore_add_server_command":"ias",  //type this command in any channel in the guild you would like to ignore the guild.
"ignore_del_command":"id"           //type this command in the channel of the dm/guild you would like to unignore.
}
```
***
### How to obtain your token
**1.** Press **Ctrl+Shift+I** (⌘⌥I on Mac) on Discord to show developer tools<br/>
**2.** Navigate to the **Application** tab<br/>
**3.** Select **Local Storage** > **https://discordapp.com** on the left<br/>
**4.** Press **Ctrl+R** (⌘R) to reload<br/>
**5.** Find **token** at the bottom and copy the value<br/>
***
### Disclaimer
This is a self-bot which is against Discord ToS. Use it at your own risk.



