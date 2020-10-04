#!/usr/bin/python3

# pdb-ez.py
# Sabi. Simple, Lightweight, but Not Beautiful

# This program consumes an easy config file and produces JSON
# files for use with the pixiv-discord-bot from Carter Yagemann.
# You can get pixiv-discord-bot here:
# https://github.com/carter-yagemann/pixiv-discord-bot/

import os
import sys

version = 1.0

cwd = os.path.abspath(os.path.dirname(__file__)) + "/"

def readEZconfig():
    cat = ""
    bigDict = {}
    with open(cwd + "ez.conf", "r") as ez:
        for line in ez.readlines():
            
            # Skip comments
            if line[0] == "#":
                continue

            # Categories are identified by square brackets
            if line[0] == "[":
                cat = line.strip()
                bigDict[cat] = {}
                bigDict[cat]["tag"] = []
                bigDict[cat]["discord"] = []
                continue
            
            # Key: Category, Value: Dictionary of Pixiv Tags
            elif "=" in line:
                l = line.split(" = ")

                # value is list of tags for each series
                if l[0] == "tag":
                    bigDict[cat]["tag"].append(l[1].strip())
                    continue

                # value is list of discord servers pics will be posted to
                elif l[0] == "discord":
                    bigDict[cat]["discord"].append(l[1].strip())
                    continue
                        
                # all other pixiv tags
                else:
                    bigDict[cat][l[0]] = l[1].strip()

    # Confirm each tag exists
    for cat in bigDict.keys():

        if "discord" not in bigDict[cat].keys():
            print("Pics will currently not be posted because a Discord server was not provided")
            bigDict[cat]["discord"] = []
        
        if "R18" not in bigDict[cat].keys() and "r18" not in bigDict[cat].keys():
            bigDict[cat]["r18"] = "no"
        
        if "R18g" not in bigDict[cat].keys() and "r18g" not in bigDict[cat].keys():
            bigDict[cat]["r18g"] = "no"

        if "manga" not in bigDict[cat].keys():
            bigDict[cat]["manga"] = "no"

        if "wildcard" not in bigDict[cat].keys():
            bigDict[cat]["wildcard"] = "no"
        
        if "series" not in bigDict[cat].keys():
            print(cat + " will not be run because it is a missing a series tag")
            bigDict[cat]["series"] = ""

        if "tag" not in bigDict[cat].keys():
            print("There are not any tags to search against within " + cat)
            bigDict[cat]["tag"] = []

    return bigDict

def basicCreds():
    with open(cwd + "pixiv.creds","w") as creds:
        creds.write("username_here\n")
        creds.write("password_here\n")

def basicEZconfig():
    with open(cwd + "ez.conf","w") as ez:
        ez.write("""# Here are the available options
# The only required things are that you
# must include the 'series' tag and 'tag' tag
# You must also put the broad category in brackets.
# The broad category can be in English
#
# Minimal Configuration Example:
# [evangelion]
# series = 新世紀エヴァンゲリオン
# tag = エヴァンゲリオン
# discord = https://discord.com/yaddayaddayadda
#
# Optional Configuration Example:
# [evangelion]
# series = 新世紀エヴァンゲリオン
# tag = エヴァンゲリオン
# tag = アスカ
# tag = 綾波レイ
# wildcard = no
# r18 = no
# r18g = no
# manga = no
# discord = https://discord.com/yaddayaddayadda
\n
""")

def writeEZconfig(bigDict):
    basicEZconfig()
    with open(cwd + "ez.conf","a") as ez:
        for cat in bigDict.keys():
            main_tags = list(bigDict[cat].keys())
            main_tags.remove("tag")
            main_tags.remove("discord")
            main_tags.sort()
            ez.write(cat + "\n")
            for tag in bigDict[cat]["tag"]:
                ez.write("tag = " + tag + "\n")
            for discord in bigDict[cat]["discord"]:
                ez.write("discord = " + discord + "\n")
            for mt in main_tags:
                ez.write(mt + " = " + str(bigDict[cat][mt]) + "\n")
            ez.write("\n")

def readCreds(bigDict):
    with open(cwd + "pixiv.creds", "r") as credFile:
        bigDict['user'] = credFile.readline().strip()
        bigDict['password'] = credFile.readline().strip()

def writePDBconfig(bigDict):
    for cat in bigDict.keys():
        if cat == 'user' or cat == 'password':
            continue
        with open(cwd + cat[1:-1] + ".json","w") as conf:
            conf.write('{\n')
            conf.write('"pixiv_username": "' + bigDict['user'] + '",\n')
            conf.write('"pixiv_password": "' + bigDict['password'] + '",\n')
            conf.write('"discord_hook_urls": [\n')
            for i in range(len(bigDict[cat]["discord"])):
                if i != len(bigDict[cat]["discord"]) - 1:
                    conf.write('"' + bigDict[cat]["discord"][i] + '",\n')
                else:
                    conf.write('"' + bigDict[cat]["discord"][i] + '"\n')
            conf.write('],\n')
            conf.write('"main_tag": "' + bigDict[cat]['series'] + '",\n')
            conf.write('"sub_tags": [\n')
            for i in range(len(bigDict[cat]["tag"])):
                if i != len(bigDict[cat]["tag"]) - 1:
                    conf.write('["' + bigDict[cat]["tag"][i] + '","Found","Missed"],\n')
                else:
                    conf.write('["' + bigDict[cat]["tag"][i] + '","Found","Missed"]\n')
            conf.write('],\n')

            if bigDict[cat]["wildcard"] == "yes":
                conf.write('"wildcard": true,\n')
            else:
                conf.write('"wildcard": false,\n')
            
            if bigDict[cat]["manga"] == "yes":
                conf.write('"allow_manga": true,\n')  
            else:
                conf.write('"allow_manga": false,\n')  
            
            if bigDict[cat]["r18"] == "yes":
                conf.write('"allow_R18": true,\n')
            else:
                conf.write('"allow_R18": false,\n')

            if bigDict[cat]["r18g"] == "yes":
                conf.write('"allow_R18-G": true\n')  
            else:
                conf.write('"allow_R18-G": false\n')  

            conf.write('}')

def main():
    if not os.path.isfile(cwd + "ez.conf"):
        basicEZconfig()
    if not os.path.isfile(cwd + "pixiv.creds"):
        basicCreds()
        sys.exit("""
        Write a configuration for each series in the ez.conf file
          Minimal Configuration Example:
          [evangelion]
          series = 新世紀エヴァンゲリオン
          tag = エヴァンゲリオン
          discord = "http://discord.com/yaddayaddayadda

        Store your username and password in pixiv.creds
          sabi
          youll_never_guess_and_shouldnt_try_5318008
          """)
    bigDict = readEZconfig()
    writeEZconfig(bigDict)
    readCreds(bigDict)
    writePDBconfig(bigDict)

# Start Program
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h","--help"]:
            sys.exit("""
            Write a configuration for each series in the ez.conf file
              Minimal Configuration Example:
              [evangelion]
              series = 新世紀エヴァンゲリオン
              tag = エヴァンゲリオン
              discord = http://discord.com/yaddayaddayadda

            Store your username and password in pixiv.creds
              sabi
              youll_never_guess_and_shouldnt_try_5318008

            Each time you run this program. The proper JSON files
            will be generated for use with pixiv-discord-bot.
              """)
        if sys.argv[1] in ["-v","--version"]:
            sys.exit(version)

    if not sys.version_info[0] == 3:
        sys.exit("This program is only compatible with Python 3")
    main()
