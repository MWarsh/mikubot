# isla.py: IRC bot 
#----
# Programmed by: Matthew Warshaw
# Date: 2015 April 13,
#----
# TO-DO
# (1) write a function to take care of creating a JSON file
#     if config.json doesn't exist
#
#
#--------------------------------------------------------------

import socket, json, sys

try:
    # reading in config data stored as a JSON file
    json_data = open("config.json").read()

    # convert RAW data to python readable
    data = json.loads(json_data)

# TODO (1)
except FileNotFoundError:
    print("ERROR: File not found")
    error_input=input("Would you like to create one? (yes or no): ")
    if error_input == 'yes':
        print("too bad :-D")
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


