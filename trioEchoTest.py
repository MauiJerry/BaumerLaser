# test Trio UDP Socket with binary echo server
import sys
this = sys.modules[__name__]
#import socket
import trio
import struct
import datetime
import random
import json
import math
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_address = ('127.0.0.1', 10001)
secondsToRun = 60

async def serverLoop():
    print("serverLoop begin")
    # Create a TCP/IP socket
    startTime = datetime.datetime.now()
    endTime = startTime + datetime.timedelta(seconds=secondsToRun)
    print("Servers starts at", startTime)
    print("Servers will end at", endTime)

    sock = trio.socket(
        family=trio.socket.AF_INET,   # IPv4
        type=trio.socket.SOCK_DGRAM,  # UDP
        )
    # Bind the socket to the port
    print('starting server on %s port %s' % server_address)
    #sock.bind(server_address)
    while True:
        curTime = datetime.datetime.now()
        if curTime > endTime:
            print("End Server Loop")
            break
        print('\nwaiting to receive message')
        data, address = await sock.recvfrom(4096)

        print('received %s bytes from %s' % (len(data), address))
        print(data)

        if data:
            sent = await sock.sendto(data, address)
            print('sent %s bytes back to %s' % (sent, address))
    sock.close()
    print("serverLoop ends")

###########################
# client
async def clientLoop():
    print('begin client loop')
    # Create a UDP socket
    sock = trio.socket(trio.socket.AF_INET, trio.socket.SOCK_DGRAM)
    sock.bind(server_address)
    message = 'This is the message.  It will be repeated.'
    startTime = datetime.datetime.now()
    endTime = startTime + datetime.timedelta(seconds=secondsToRun)

    while True:
        curTime = datetime.datetime.now()
        if curTime > endTime:
            print("End Server Loop")
            break
        # Send data
        print (sys.stderr, 'sending "%s"' % message)
        sent = sock.sendto(message, server_address)

        # Receive response
        print (sys.stderr, 'waiting to receive')
        data, server = sock.recvfrom(4096)
        print (sys.stderr, 'received "%s"' % data)
        trio.sleep(1)
    print ('end client loop')
    sock.close()

async def trioEchoTest():
    print("trioEchoTest begin")
    async with trio.open_nursery() as nursery:
        # first we spawn the sender
        nursery.start_soon(serverLoop)
        await trio.sleep(2)
        #nursery.start_soon(clientLoop)
        print("Ok started both of those")
    print("trioEchoTest ended")

if __name__ == "__main__":
    print("Trio Echo Test")
    trio.run(trioEchoTest)

