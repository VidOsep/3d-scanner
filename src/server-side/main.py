#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import picamera
import RPi.GPIO as GPIO
import time
import atexit
import socket

# Camera for taking pictures
camera = picamera.PiCamera()

# Laser control
PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN,GPIO.OUT)

# Stepper intialization
mh = Adafruit_MotorHAT(addr=0x60)
atexit.register(turnOffMotors)
myStepper = mh.getStepper(200, 1)
myStepper.setSpeed(30)

# TCP communication
HOST = "192.168.1.100"
PORT = 42069
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(1)
(conn, addr) = s.accept()


def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

def testHardware():
    """ Tests the stepper motor and laser """
    myStepper.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.STEP)
    time.sleep(1)
    myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.STEP)
    time.sleep(1)
    GPIO.output(PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(PIN, GPIO.LOW)

def normalScan(resolution=100):
    """ Scans whole object, announces completion to server """
    for i in range(resolution):
        camera.capture('image' + str(i) + ".jpg")
        time.sleep(0.1)
        GPIO.output(PIN, GPIO.HIGH)
        camera.capture('subimage' + str(i) + ".jpg")
        time.sleep(0.1)
        GPIO.output(PIN, GPIO.LOW)
        myStepper.step(1, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)

def LBLScan():
    """ Scans object line by line, sends each pair of images indiviudally"""
    # TODO
    return

while True:
    data = conn.recv(1024) # Read incoming commands from pc

    if data=="start-scan-normal":
        normalScan()
        s.send(b"finished")
    elif data=="start-scan-lbl":
        pass
    elif data=="test":
        testHardware()
        s.send(b"finished")
    elif data=="quit":
        break
