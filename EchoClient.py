import socket
import sys
#
# # Create a TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# # Bind the socket to the port
# server_address = ('localhost', 10000)
# print (sys.stderr, 'starting up on %s port %s' % server_address
# sock.bind(server_address)
#
# while True:
#     print ( sys.stderr, '\nwaiting to receive message'
#     data, address = sock.recvfrom(4096)
#
#     print ( sys.stderr, 'received %s bytes from %s' % (len(data), address)
#     print ( sys.stderr, data
#
#     if data:
#         sent = sock.sendto(data, address)
#         print ( sys.stderr, 'sent %s bytes back to %s' % (sent, address)

###########################
# client
import socket
import sys
import time

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('127.0.0.1', 10001)
message = b'This is the message.  It will be repeated.'
print("Client sending messages to ", server_address)
try:
    for x in range(0, 10):
        # Send data
        print (sys.stderr, 'sending "%s"' % message)
        sent = sock.sendto(message, server_address)

        # Receive response
        print (sys.stderr, 'waiting to receive')
        data, server = sock.recvfrom(4096)
        print (sys.stderr, 'received "%s"' % data)
        time.sleep(1)

finally:
    print (sys.stderr, 'closing socket')
    sock.close()


