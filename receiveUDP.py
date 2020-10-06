import socket

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('192.168.2.250',1234))
while(1):
    d,a = s.recvfrom(4096)
    print("got from ",a)