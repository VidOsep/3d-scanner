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
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

# Stepper intialization
mh = Adafruit_MotorHAT(addr = 0x60)
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
 
def normalScan(resolution=100):
    """ Scans whole object, announces completion to server """
    for i in range(resolution)
        camera.capture('image' + str(i) + ".jpg")
        time.sleep(0.1)
        GPIO.output(18, GPIO.HIGH)
        camera.capture('subimage' + str(i) + ".jpg")
        time.sleep(0.1)
        GPIO.output(18, GPIO.LOW)
        myStepper.step(1, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)


def LBLScan():
    """ Scans object line by line, sends each pair of images indiviudally"""
    # TODO
    return



for i in range(100):
    myStepper.step(1, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
    camera.capture('image' + str(i) + ".jpg")
    print("1#taken")
    time.sleep(0.2)	
    GPIO.output(18,GPIO.HIGH)
    camera.capture('subimage' + str(i) + ".jpg")
    time.sleep(0.2)
    GPIO.output(18,GPIO.LOW)
