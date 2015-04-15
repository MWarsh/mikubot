# isla.py: IRC bot 
#----
# Programmed by: Matthew Warshaw
# Date: 2015 April 13,
# Done?: NOPE
#----
# NOTES
# (1) Parsing will not work if user's tab complete does [nick], instead of
#       [nick]:    I don't want to fix this, fix YOUR IRC client instead
#-----
# TO-DO
# (1) alter the exception to write user input data to a JSON file
# (2) think if I should put more in the join function
# (3) This is where I would implement NLP (natural language processing)
# (4) Change the class structure to allow for a "dev" mode, where this
#       formatted output will then be printed
#-----------------------------------------------------------------------
#
# From Last time:
#  Having issue with checking data to see if PRIVMSG appears
#   -- data doesn't get parsed, but is directly sent to error.txt
#
#########################################################################
from __future__ import print_function

import socket
import json
import sys
import time

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
        self.send("NICK %s" % (self.nick))
        self.send("USER %s %s %s :%s\r\n" % (
                self.user, self.user, self.user, self.nick))
        self.join(self.chans['moe'])
        
        
    def join(self, chan):
        ''' I figured it would be better to have join as a separate function '''    
        self.send("JOIN %s" % chan)
        # not sure what else to put here TODO (2)

        # to keep connection to IRC alive

    def output(self, data):
        ''' used for dev purposes, easily prints data to terminal '''
        print(data)
        
    def msg(self, msg, chan):
        ''' To make the sending of messages easier '''
        self.send('PRIVMSG %s : %s' % (msg, self.chans['moe']))
        
    def listen(self):
        ''' Respond to PING, and general function for life of bot '''
        
        data = bytes.decode(self.irc.recv(4096))
        
        if data.startswith("PING"):
            self.send("PONG " + data.split(" ")[1])    
        
        # I found this method of checking when to parse to be the easiest
        # it provides for a more rubst soltion then what I've thought of so far
        #startingPoint = 'PRIVMSG %s'
        if 'PRIVMSG %s' % (self.chans['moe']) in data:
            print(data)
            self.parse(data)
        else:
            pass
    
    def parse(self, data):
        ''' To intrepet RAW IRC data, this is important '''
        raw = data
        data = data.rstrip('\r\n')
        data = data.split(":")
        del data[0]
        
        msgTime = time.localtime()
        
        # un-directed speech in IRC; no use of "[nick]:"
        if(len(data) == 2):
            msg = data[1]
            chan = data[0].split(' ')[2]
            fromNick = data[0].split(' ')[0].split('!')[0]
            # for clean output to terminal for dev purposes  TODO (4)
            #print("[%02i:%02i:%02i] %s: %s" % (
            #    msgTime[3], msgTime[4], msgTime[5], fromNick, msg))
            
            
            print("[%02i:%02i:%02i] %s: %s" % (
                    msgTime[3], msgTime[4], msgTime[5], fromNick, msg))
            
            
            #################### mention from GROOT ###########################
            #print("[{m[3]:02i}:{m[4]:02i}:{m[5]}] {fn}:{ms}".format(m=msgTime, 
            #                fn=fromNick, ms=msg))
            ###################################################################
            
            if self.nick in msg:
                self.msg("Who dare calls upon me", self.chans['moe'])
            elif "heh" in msg:
                self.msg("heh\nheh\nheh heh", self.chans['moe'])

        
        # in this case, a nick was directly referred to
        elif(len(data) == 3):
            msg = data[2]
            chan = data[0].split(' ')[2]
            fromNick = data[0].split(' ')[0].split('!')[0]
            toNick = data[1]
            
            # for clean output to terminal for dev purposes  TODO (4)
            print("[%02i:%02i:%02i] %s:%s %s" % (msgTime[3], 
                    msgTime[4], msgTime[5], fromNick, toNick, msg))
                    
            if self.nick in toNick:
                self.msg("Hi", self.chans['moe'])
                
           
        
        # error handling case, for life's little surprises 
        else:
            print("I'm fucking lost")
            f=open("error.txt", "w+")
            for item in data:
                f.write("%s\r" %(item))
            f.write("I don't know how to handle this\n")
            f.close()
            sys.exit("\n\nERROR: un-Parseable IRC data")
            
        
    def searchlist(self, list, key):
        for item in list:
            if item.find(key):
                return True
            else:
                return False
        
    def close(self):
        self.msg("Bye everyone!!", self.chans['moe'])
        self.irc.close()
        sys.exit("\nProgram Terminated...")
        
        


if __name__ == '__main__':
    Isla = Bot()
    Isla.connect()
    while True:
        try:
            Isla.listen()
        except KeyboardInterrupt:
            Isla.close()
        
