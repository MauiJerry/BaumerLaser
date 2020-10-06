# Baumer OM-70 test using Trio Sockets
# default ip address is 198.162.0.250
# our rPi is on a dedicated switch on the 198.162.2.x network
# so that needs to be changed
import sys
this = sys.modules[__name__]
import trio
import struct
import datetime
import random
import json
import math
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

from BaumerOM70 import OM70Datum

def keyForDistance ():
    return "DistanceMM"
def keyForTimeStamp():
    return "Timestamp"
def keyForQuality():
    return "Quality"
def keyForAlarmState():
    return "AlarmState"
def keyForSwitchState():
    return "SwitchState"

# address is set in web interface "Process Interface
baumer_udpAddr = ("192.168.2.150", 1234)
baumer_udpAddr = ('127.0.0.1', 1234)

class BaumerOM70Test():
    # needs a byte buffer or two for receive
    # has data  items
    def __init__(self, udpAddrP = this.baumer_udpAddr):
        # Create a UDP socket__baumer_ipPort
        # make two for double buffering?
        self.datum1 = OM70Datum.OM70Datum()
        self.datum2 = OM70Datum.OM70Datum()
        self.buffer = bytearray(self.datum1.byteSize())
        self.buffSize = self.datum1.byteSize()
        self.udpAddr = udpAddrP

    async def receiveData(self, moveOnTime=30):
        udp_sock = trio.socket.socket(
            family=trio.socket.AF_INET,  # IPv4
            type=trio.socket.SOCK_DGRAM,  # UDP
        )
        udp_sock.bind(self.udpAddr)
        with trio.move_on_after(moveOnTime):
            while True:
                # recvfrom
                data, address = await udp_sock.recv(self.buffSize)
                print("Got response from:", address)
                self.datum2.fromBuffer(data)
                print("Data: ", self.datum2.asTuple(), self.datum2.asJson())

    async def sendDataLoop(self, moveOnTime=30):
        send_sock = trio.socket.socket(
            family=trio.socket.AF_INET,  # IPv4
            type=trio.socket.SOCK_DGRAM,  # UDP
        )
        with trio.move_on_after(moveOnTime):
            self.datum1.setTestRandom()
            print("send Random DM70 : ", self.datum1.asTuple(), self.datum1.asJson())
            self.datum1.toBuffer(self.buffer)
            send_sock.sendto(self.buffer, self.udpAddr)

def testDatumPackUnpack():
    print("testDatumPackUnpack  begin")
    b1 = OM70Datum.OM70Datum()
    b2 = OM70Datum.OM70Datum()
    print("b1:",b1)
    print("b2:",b2)
    t = b1.asTuple()
    print ("tuple",t)
    if b1.equals(b2):
        print("B1=B2")
    else:
        print("B1 not = B2")
    b2.setTestRandom()
    b1.setTest1()
    print("b1 Test:",b1.asTuple())
    print("b2 Random:",b2.asTuple())
    if b1.equals(b2):
        print("B1=B2")
    else:
        print("B1 not = B2")
    print("b1 json:", b1.asJson())
    print("b2 json:", b2.asJson())
    buffer = bytearray(b1.byteSize())
    print("Now try converting to/from buffer")
    b1.toBuffer(buffer)
    print("buffer:", buffer)
    b2.fromBuffer(buffer)
    print("b1 to   buffer", b1.asTuple())
    print("b2 from Buffer", b2.asTuple())
    if b1.equals(b2):
        print("B1=B2")
    else:
        print("B1 not = B2")
    print("b2 from buffer as json", b2.asJson())
    print("testDatumPackUnpack  end")

async def testSendRcv(baumer):
    print ("testSendRcv begin")
    moveonTime = 30
    async with trio.open_nursery() as nursery:
        # first we spawn the sender
        nursery.start_soon(baumer.sendDataLoop, nursery)

        # now we try
        try:
            udp_sock = trio.socket.socket(
                family=trio.socket.AF_INET,  # IPv4
                type=trio.socket.SOCK_DGRAM,  # UDP
            )
            udp_sock.bind(baumer_udpAddr)
            with trio.move_on_after(moveonTime*2):
                while True:
                    # recvfrom
                    data, address = await udp_sock.recvfrom(baumer.buffSize)
                    print("Got response from:", address)
                    baumer.datum2.fromBuffer(data)
                    print("Data: ", baumer.datum2.asTuple(), baumer.datum2.asJson())
        except trio.Cancelled:
           log.warning("***Trio propagated Cancelled main, time to die")
        except:
            log.error("Exception caught in the nursery loop: ", exc_info=True)
            print("Exception somewhere in modac_io_server event loop.")
    print ("testSendRcv end")

if __name__ == "__main__":
    print("Test Baumer OM70 distance Sensor")
    testDatumPackUnpack()

    #baumer = BaumerOM70()
    #trio.run(baumer.receiveData)
    #trio.run(testSendRcv, baumer)
