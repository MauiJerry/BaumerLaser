import socket

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(("", 37020))
while(1):
    data, addr = s.recvfrom(1024)
    print("received message from", addr)
    print("   message: %s"%data)


