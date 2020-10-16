# Baumer OM-70 test using Trio Sockets
# default ip address is 198.162.0.250
# our rPi is on a dedicated switch on the 198.162.2.x network
# so that needs to be changed
import sys
this = sys.modules[__name__]
import socket
import datetime
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

import struct

from BaumerOM70 import OM70Datum

# address is set in web interface "Process Interface
port = 12345
baumer_udpAddr = ('192.168.2.250', port )
baumer_udpAddr = ('', port)

def disectPacket(data):
    print("Packet", data)
    idLittle = struct.unpack('<I',data[0:4])
    idBig = struct.unpack('>I',data[0:4])
    print("  Id:", idLittle, idBig)

def receiveOm70Data():
    print("Begin receiveOm70Data ", baumer_udpAddr)
    try:
        # udp_sock = socket.socket(
        #     socket.AF_INET,  # IPv4
        #     socket.SOCK_DGRAM,  # UDP
        # )
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_sock.bind(baumer_udpAddr)
    except:
        log.error("Exception caught creating socket: ", exc_info=True)
        return
    datum = OM70Datum.OM70Datum()
    buffer = bytearray(datum.byteSize())
    buffSize = datum.byteSize()
    while True:
        # recvfrom
        try:
            data, address = udp_sock.recvfrom(buffSize)
            print("Received data from:", address)
            print("  raw:", data)
            disectPacket(data)
            datum.fromBuffer(data)
            print("  OM70: ", datum.asTuple())
            #print("  OM70: ", datum.fullJsonIndent())
            print("  OM70: ", datum.asJson())
        except:
            log.error("Exception caught in Forever Loop: ", exc_info=True)
            break
    print("End receiveOm70Data")


if __name__ == "__main__":
    print("Receive Client for Baumer OM70 distance Sensor")
    receiveOm70Data()
