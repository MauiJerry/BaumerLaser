# broadcast Sender test from gits.github.com/cry Python udp broadcast client server example, modified
import socket
import time

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# set a timeout so socket doesnt block indefinitely while awaiting data
# how will this work under Trio/async
s.settimeout(0.2)
s.bind(("", 44444))
message = b'mary had a little lamb'
count = 0
while True:
    count += 1
    s.sendto(message, ('<broadcast>', 37020))
    print("sent message  ",count)
    time.sleep(1)
