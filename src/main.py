import socket
import os
import time

# Setting up the pc/raspi connection
HOST = "192.168.1.100"  # Raspberry pi IP
PORT = 42069
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False

def connect():
    """ Establish a connection between the raspberry pi and the pc """
    global connected
    # Run the server side script on the raspberry pi
    os.system("ssh pi@%s nohup python server.py &"%HOST)  # Make sure your pi's ssh server is passwordless
    # Establish the connection
    s.connect((HOST, PORT))
    reply = s.recv(1024)
    if reply == "Connected":
        print("Successfuly connected!")
        connected = True

def startNormalScan():
    # Check if device connected
    if not connected:
        print("Raspberry pi not connected!")
        return
    # Give signal to start scan
    s.send(b"start-scan-normal")
    data = s.recv(1024)  # Wait for completion on server side
    if data == "finished":
        print("Successful scan")

def testHardware():
    # Check if device connected
    if not connected:
        print("Raspberry pi not connected!")
        return
    # Give signal to start test
    s.send(b"test")
    data = s.recv(1024) # Wait for completion on server side
    if data == "finished":
        print("Successful test")

def quit():
    # Check if device connected
    if not connected:
        print("Raspberry pi not connected!")
        return
    # Give signal to quit
    s.send(b"quit")


print("Connect - connect\nStart Normal Scan - ns\nTest Hardware - test\nQuit - quit")
while True:
    cmd = input("->")
    if cmd=="connect":
        connect()
    elif cmd=="ns":
        startNormalScan()
    elif cmd=="test":
        testHardware()
    elif cmd=="lbls":
        continue
    elif cmd=="quit":
        quit()
        break