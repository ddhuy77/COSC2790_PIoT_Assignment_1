import bluetooth
from socket import *
#server
hostMACAddress = '34:DE:1A:31:2B:52' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 4
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind((hostMACAddress, port))
s.listen(backlog)
try:
    client, clientInfo = s.accept()
    while 1:
        data = client.recv(size)
        if data:
            print(data)
            client.send(data) # Echo back to client
except:	
    print("Closing socket")
    client.close()
    s.close()