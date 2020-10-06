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

from BaumerOM70 import OM70Datum

# address is set in web interface "Process Interface
baumer_udpAddr = ('192.168.2.250', 1234)
#baumer_udpAddr = ('0.0.0.0', 1234)
#baumer_udpAddr = (' ', 1234)
#baumer_udpAddr = ('127.0.0.1',1234)

def receiveOm70Data():
    print("Begin receiveOm70Data")
    try:
        udp_sock = socket.socket(
            socket.AF_INET,  # IPv4
            socket.SOCK_DGRAM,  # UDP
        )
        udp_sock.bind((' ',1234))#baumer_udpAddr)
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
            datum.fromBuffer(data)
            print("Data: ", datum.asTuple(), datum.asJson())
        except:
            log.error("Exception caught in Forever Loop: ", exc_info=True)
            break
    print("End receiveOm70Data")


if __name__ == "__main__":
    print("Receive Client for Baumer OM70 distance Sensor")
    receiveOm70Data()
