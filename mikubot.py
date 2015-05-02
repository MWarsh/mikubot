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
# (5) Handle the case where the bot's nick is already taken
# (6) Take precaution to avoid flooding the network
#       ideas:  (a) implement a queue to handle commands to bot
#               (b) if queue becomes filled, delete all contents
#               (c) wait for 5s (not definite) to respond to commands
# (7) take care when the server issues a NOTICE
#-----------------------------------------------------------------------
# Issues:
#   cleanup how the error file is made
#   ONLY USE SSL MODE (for now....)
#
#########################################################################
from __future__ import print_function

import socket
import json
import sys
import time
import ssl

class Bot:
    
    def __init__(self, config='config.json'):
        
        try:
            # reading in config data stored as a JSON file
            json_data = open(config).read()
        except FileNotFoundError:
            print("ERROR: File not found")
            error_input=input("Would you like to create one? (yes or no): ")
            if error_input == 'yes':
                self.config = {}
                self.config['nick'] = input("Nick: ")
                self.config['user'] = input("User: ")
                self.config['ssl'] = input("SSL? (True or False): ")
                self.config['network'] = input("network domain: ")
                self.config['porn'] = input("Port: ")
                self.config['chan'] = input("Chan: ")
                # TO-DO (1)
            else:
                sys.exit("BAKA!!")

        # Bot's personal info 
        # convert RAW JSON data to python readable
        self.config = json.loads(json_data) # data is a dict type
        self.ircNetwork = (self.config['network']['freenode'], self.config['port'] )

    def send(self, msg):
        ''' Simplifies the sending of encoded data to IRC internets '''
        self.irc.send(str.encode("{m}\r\n".format(m=msg)))
         
    def connect(self):
        ''' To begin the connection procedure '''
        
        if self.config['ssl']:
            self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.irc.connect(self.ircNetwork)
            self.irc = ssl.wrap_socket(self.irc)
        else:
            self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.irc.connect(self.ircNetwork)
        
        self.send("NICK {n}".format(n=self.config['nick']))
        self.send("USER {u} {u} {u} :{n}".format(u=self.config['user'], n=self.config['nick']))
        self.join(self.config['chans']['moe'])
        
        self.msg("identify hello_there", "nickserv")
        
        
    def join(self, chan):
        ''' I figured it would be better to have join as a separate function '''    
        self.send("JOIN {c}".format(c=chan))
        # not sure what else to put here TODO (2)

        # to keep connection to IRC alive
    def part(self,chan):
        ''' To tell the bot to leave a given irc channel'''
        self.send("PART {c}".format(c=chan))
        
        
    def output(self, data):
        ''' used for dev purposes, easily prints data to terminal '''
        print(data)
        
    def msg(self, msg, chan):
        ''' To make the sending of messages easier '''
        self.send('PRIVMSG {c} :{m}'.format(m=msg, c=self.config['chans']['moe']))
        
    def listen(self):
        ''' Respond to PING, and general function for life of bot '''
        
        data = bytes.decode(self.irc.recv(4096))
        print("raw->{d}".format(d=data))
        
        if data.startswith("PING"):
            self.send("PONG " + data.split(" ")[1])    
        
        if 'PRIVMSG %s' % (self.config['chans']['moe']) in data:
            #print(data)
            self.parse(data)
        else:
            pass
    
    def parse(self, data):
        ''' To intrepet RAW IRC data, this is important '''
        raw = data # might be good to save, idk really...
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
            print("[{m[3]:02d}:{m[4]:02d}:{m[5]}] {fn}: {ms}".format(
                    m=msgTime, fn=fromNick, ms=msg))
            
            #################### mention from GROOT ###########################
            #print("[{m[3]:02d}:{m[4]:02d}:{m[5]}] {fn}:{ms}".format(m=msgTime, 
            #                fn=fromNick, ms=msg))
            ###################################################################
            print("msg->{m}".format(m=msg))
            if "heh" in msg:
                self.msg("heh", self.config['chans']['moe'])
                self.msg("heh", self.config['chans']['moe'])
                self.msg("heh heh", self.config['chans']['moe'])
                time.sleep(1)   # TODO (6)
                
            elif self.config['nick'] in msg:
                self.msg("Who dare calls upon me", self.config['chans']['moe'])
     
        # in this case, a nick was directly referred to
        elif(len(data) == 3):
            msg = data[2]
            chan = data[0].split(' ')[2]
            fromNick = data[0].split(' ')[0].split('!')[0]
            toNick = data[1]
            
            # for clean output to terminal for dev purposes  TODO (4)    
            print("[{m[3]:02d}:{m[4]:02d}:{m[5]}] {fn}: {tn} {ms}".format(
                m=msgTime, fn=fromNick, tn=toNick, ms=msg))
            
            print("msg->{m}".format(m=msg))
            
            if "heh" in msg:
                self.msg("heh", self.config['chans']['moe'])
                self.msg("heh", self.config['chans']['moe'])
                self.msg("heh heh", self.config['chans']['moe'])
                time.sleep(1)   # TODO (6)
                
                
            elif self.config['nick'] in toNick:
                self.msg("Hi", self.config['chans']['moe'])
                print(raw)
                if "join" in msg:
                    channel = msg.split(' ')[1]
                    self.join(channel)
                elif "part" in msg:
                    channel = msg.split(' ')
                    self.part(channel)
        
        # error handling case, for life's little surprises 
        else:
            print("I'm fucking lost")
            date = "{m[0]}/{m[1]}/{m[2]} - ({m[3]:02d};{m[4]:02d};{m[5]})".format(
                m=msgTime)
            f=open("error_{s}.rtf".format(s=date), "w")
            # f=open("error_{m[0]} / {m[1]} / {m[2]}, -- 
            #   [{m[3]:02d};{m[4]:02d};{m[5]}].txt".format(m=msgTime ), "w+")
            
            for item in data:
                f.write("%s\r" %(item))
            f.write("I don't know how to handle this\n")
            sys.exit("\n\nERROR: un-Parseable IRC data")
            
        
    def searchlist(self, list, key):
        for item in list:
            if item.find(key):
                return True
            else:
                return False
        
    def close(self, chan):
        self.msg("Adieu", chan)
        self.irc.close()
        sys.exit("\nProgram Terminated...")
        
        


if __name__ == '__main__':
    Isla = Bot()
    Isla.connect()
    while True:
        try:
            Isla.listen()
        except KeyboardInterrupt:
            Isla.close(Isla.config['chans']['moe'])
        
