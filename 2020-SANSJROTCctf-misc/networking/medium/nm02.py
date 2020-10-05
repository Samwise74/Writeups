import socket

s = socket.socket()
s.connect(('jrotc-nm02.allyourbases.co', 9010))
while 1:
    a = s.recv(32)
    print(a[:-3])
    b = (str(round(eval(a[:-3]))) + '\n').encode()
    print(b)
    s.send(b)
    print(s.recv(32))
