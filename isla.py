# isla.py: IRC bot 
#----
# Programmed by: Matthew Warshaw
# Date: 2015 April 13,
#----
# TO-DO
# (1) alter the exception to write user input data to a JSON file
# (2) think if I should put more in the join function
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

            # convert RAW JSON data to python readable
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
        
        self.nick = data['nick']
        self.user = data['user']
        self.network = data['network']  # be aware this a dict object
        self.port = data['port']
        self.chans = data['channels']
        self.ircNetwork = (self.network['freenode'], data['port'])

    def send(self, msg):
        ''' Simplifies the sending of RAW data to IRC internets '''
        self.irc.send(str.encode(msg + "\r\n"))
         
    def connect(self):
        ''' To begin the connection procedure '''
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect(self.ircNetwork)
        self.send("NICK %s", (self.nick))
        self.send("USER %s %s %s :%s\r\n", (self.user, self.user, self.user, self.nick))
        
    def join(self, chan):
        ''' I figured it would be better to have join as a separate function '''    
        self.send("JOIN %s", chan)
        # not sure what else to put here TODO (2)

        # to keep connection to IRC alive

if __name__ == '__main__':
    Isla = Bot()
    Isla.connect()
    
