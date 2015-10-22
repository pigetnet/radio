#!/usr/bin/python
# Taken from http://www.grantjenks.com/wiki/random/python_asynchat_chat_example
# (Grant Jenks)
# Socket manager for Collectors
import asynchat
import asyncore
import socket
import os
import subprocess
import threading


global messageBuffer
messageBuffer = False


class SocketHandler(asynchat.async_chat):
    def __init__(self, sock):
        print "Starting SocketHandler"
        asynchat.async_chat.__init__(self, sock=sock, map=chat_room)

        self.set_terminator('\n')
        self.buffer = []

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    # When a message arrived broadcast it
    def found_terminator(self):
        global messageBuffer
        msg = ''.join(self.buffer)
        print 'Socket Broadcast:', msg
        for handler in chat_room.itervalues():
            if hasattr(handler, 'push'):
                handler.push(msg + '\n')
        self.buffer = []

        if msg.strip() == "stop":
            print "Closing collector : Socket"
            server.close()
            os._exit(0)
        else:
            messageBuffer = msg.strip()


class SocketServer(asyncore.dispatcher):
    def __init__(self, host, port):
        print "Starting SocketServer"
        asyncore.dispatcher.__init__(self, map=chat_room)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = SocketHandler(sock)


class Start():
    def __init__(self, port):
        global chat_room
        chat_room = {}
        thread_socket = threading.Thread(
            target=self.thread_start,
            args=(port,)
        )
        thread_socket.start()

    def thread_start(self, port):
        print "Starting Threaded Socket"
        global server
        server = SocketServer("0.0.0.0", int(port))
        # server = SocketServer('localhost', int(port))
        asyncore.loop(map=chat_room)


def Close():
        server.close()


def Send(msg):
    for handler in chat_room.itervalues():
        if hasattr(handler, 'push'):
                handler.push(msg + '\n')


def Listen():
    global messageBuffer
    message = messageBuffer
    messageBuffer = False
    return message
