from socket import *
import sys

class starto(object):
    ''''
    Class for connect and holding a bot in IRC
    '''
    def __init__(self, server, port, nick):
        self.server = server
        self.port = port
        self.nick = nick      
        
        
    ##--------------FUNCTIONS----------------##

    def command(self, cmd):
        irc.send(cmd)

    def JOIN(self, chan):
            if not chan.startswith( '#' ):
                    chan = '#%s' % chan
            cmd = "JOIN %s\r\n" % chan
            command(cmd)

    def NICK(self, nick):
        cmd = "NICK %s\r\n" %nick
        command(cmd)

    def USER (self, UserName, HostName, ServerName, RealName):
        cmd = "USER %s %s %s :%s\r\n" %(UserName, HostName, ServerName, RealName)
        command(cmd)

    def PRIVMSG(self, msg):
        cmd = "PRIVMSG %s\r\n" %msg
        command(cmd)
        
    def respond(self, message, chan=None, nick=None):
        '''
        Method for sending responses to channel or to user via /msg
        '''
        if chan:
            if not chan.startswith( '#' ):
                    chan = '#%s' % chan
            self.send('PRIVMSG %s :%s ' % (chan, message ) )
        elif nick:
            self.send('PRIVMSG %s :%s ' % (nick, message ) )
        
        

    ##---------END-OF-FUNCTIONS ------------##


    irc = socket( AF_INET, SOCK_STREAM )
    ADDR = ( NETWORK, PORT )
    irc.connect( ADDR )
    NICK(nick)
    USER(user_name, host_name, server_name, real_name)
    JOIN(CHAN)

    while True:
        data = irc.recv(4096)
        if data.find ( 'PING' ) != -1:
            irc.send ( 'PONG ' + data.split()[1] + '\r\n')

        elif data.find ( 'PRIVMSG' ) != -1:
            message = ':'.join ( data.split ( ':' ) [2: ] )

            if message.lower().find( 'hi' ) == True:
                PRIVMSG('hello')





