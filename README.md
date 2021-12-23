# eso-addon-manager
My command line interface for easily downloading, installing, and updating addons for Elder Scrolls Online on Linux.

Please note that I no longer play Elder Scrolls Online so this doesn't really get used and hasn't been ran or updated for a few years now.

As such, I don't recommend actually using this. I am kind of just putting this here to prove to recruiters that I can actually code (somewhat).

## Description

This command line interface uses a python script AddonManager.py which allows for the installation and updating of addons. The actual installation and update process is done by calling update.sh. A record of the addons and the last time that they were updated are stored in the text file ESOUIurls.txt and has a backup located at ESOUIurlsBU.txt.

## Installation

Fair warning, it has been a few years since I have played and I don't even have ESO on my computer anymore so I am working off of memory here. If I remember correctly, I had this script in the folder that had the ESO Addons. It was somewhere in my steam path (I made a symlink in my home directory to that spot to make it easier to navigate there). Just put this folder in that directory and start installing addons.

But again, I don't recommend using this.

## Executing Program

'''
python AddonManager.py -h
'''
 Has all the details.
 Make sure you use the INFO page on ESOUI for the ESO addon that you want.

## Things that I would fix if I kept using this

Well first off, I'd Check if this even still worked. Its based on regex parsing of html (yikes). If ESOUI changed its pages then it probably won't work anymore.

Also, I would add functionality for removing addons.

Would probably use a real json as well instead of just a ghetto txt file. I was being hacky with this script. Honestly I just wanted to get this program written ASAP so I could go back to playing.

## What is fix_script.sh ??

I had a problem with one of the addon's lua tables being buggy. Basically it would reset the tables. I believe I had to run it everytime that particular addon got updated. I think you could edit this script to use it to import other people's Harvest Map (that was the name of the addon I believe) data.

## Who to Blame for this Mess

Jordan Porter
