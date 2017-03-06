#!/usr/bin/env python
import Skype4Py
import sys
import os

os.environ['DISPLAY'] = ":1"

skype = Skype4Py.Skype(Transport='x11')
skype.Attach()
user = sys.argv[1]
msg = ' '.join(sys.argv[2:])
message = skype.SendMessage(user, msg)

"""
mport Skype4Py as sky 
client = sky.Skype() # Client instance 
client.Attach() # I think this allows you to use the client.  Whatever, it's required. 
client.ActiveChats[0] # I believe this is a list-like object of all active chats.  Can't remember why the index is there, but it's likely important. 
#and finally 
Skype.Chat.SendMessage(str) #
"""
