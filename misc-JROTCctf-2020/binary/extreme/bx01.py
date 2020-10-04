import time
from datetime import datetime
import pytz
import socket
from os import system, name

# Change this to the challenge based on the server time.
# It should look something like: IvkKBrth.jGkakJruwmxu.DlrBkAoohaJr.pAqorrgCkqpBC.
chal = b''
# Change this to the time it will be when the server generates the challenge.
# It should be in the format HH:MM:SS
req_time = ''

while 1:
    server_time = datetime.now(pytz.timezone(
        'Europe/London')).strftime("%H:%M:%S")
    if server_time == req_time:
        s = socket.socket()
        s.connect(('jrotc-ne02.allyourbases.co', 9012))
        s.recv(2048)
        s.send(chal)
        print(s.recv(2048))
        exit()
    else:
        print('current server time:', server_time, end="\r")
        time.sleep(0.2)
