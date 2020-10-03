# pdb-ez
Sabi. Simple, Lightweight, but Not Beautiful.

## What is it?
pdb-ez is an easy configuration generator for [pixiv-discord-bot](http://github.com/carter-yagemann/pixiv-discord-bot).
*NOTICE*: This will **delete** existing JSON files with the same name, so make sure you reflect existing configs in ez.conf

## Installation
Simply download this script and copy it to your pixiv-discord-bot directory. Then execute `python3 pdb-ez.py`.  This will generate the ez.conf file and pixiv.creds.  Follow the commented example in ez.conf and replace the username and password with your Pixiv credentials in pixiv.creds.

## How to use
- If you have a config setup, to generate or update your JSON files
  -`python3 pdb-ez.py`
- Then with your new JSON files execute pixiv-discord-bot.

## Do you need separate .conf files for each series you are scraping?
No, put all series in the one ez.conf.  

## ez.conf example
```
[evangelion]
series = 新世紀エヴァンゲリオン
tag = エヴァンゲリオン
discord = http://discord.com/yaddayaddayadda

[series 2]
series = series_tag
tag = tag_1
tag = tag_2
tag = tag_3
discord = discord_link_1
discord = discord_link_2
```
