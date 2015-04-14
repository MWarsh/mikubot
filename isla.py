# isla.py: IRC bot 
#----
# Programmed by: Matthew Warshaw
# Date: 2015 April 13,
#----
# TO-DO
# (1) alter the exception to write user input data to a JSON file
#
#
#------------------------------------------------------------------

import socket
import json
import sys


class Bot:
    
    def __init__(self, config='config.json'):
        
        try:
            # reading in config data stored as a JSON file
            json_data = open("config.json").read()

            # convert RAW data to python readable
            data = json.loads(json_data)


        except FileNotFoundError:
            print("ERROR: File not found")
            error_input=input("Would you like to create one? (yes or no): ")
            if error_input == 'yes':
                self.nick = input("Nick: ")
                self.user = input("User: ")
                self.network = input("network domain: ")
                self.port = input("Port: ")
                self.chan = input("Chan: ")
                # TO-DO (1)

            else:
                sys.exit("BAKA!!")



# Bot's personal info

nick = data['nick']
user = data['user']
network = data['network']  # be aware this a dict object
port = data['port']
chans = data['channels']

connection_info = (network['freenode'], data['port'])

# connection procedure

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect(connection_info)
irc.send(str.encode("NICK %s\r\n", (nick)))
irc.send(str.encode("USER %s %s %s :%s\r\n", (user, user, user, nick)))
irc.send("JOIN " + chans['moe'] + '\r\n')

# to keep connection to IRC alive

irc.send("PRIVMSG " + chans['moe'] + " : " "hi" + "\r\n")

while True:
    data = irc.recv(4096)

    if data.find == "PONG":
        irc.send("PONG")


