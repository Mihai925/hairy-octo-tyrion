#!/usr/bin/python
# Jaikrishna
# Initial Date: June 24, 2013
# Last Updated: June 24, 2013
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
#
# http://www.dexterindustries.com/
# This code is for testing the BrickPi with a Lego Motor

from BrickPi import *   #import BrickPi.py file to use BrickPi operations
import math

WHEELRADIUS = 2.825

BrickPiSetup()  # setup the serial port for communication

motor1 = PORT_A
motor2 = PORT_B
speed_left = 0 
speed_right = 0
no_seconds_forward = 0.75 # 30 cm
no_seconds_left = 1.3 # 90 deg

BrickPi.MotorEnable[motor1] = 1 #Enable the Motor A
BrickPi.MotorEnable[motor2] = 1 #Enable the Motor B

# Reset the motor sensor reading
BrickPi.Encoder[motor1] = 0
BrickPi.Encoder[motor2] = 0

BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

#Move Forward
def fwd(no_seconds):
  global speed_left, speed_right
  print "Going Forward"
  speed_right = 210
  speed_left = 200
  BrickPi.MotorSpeed[motor1] = speed_right
  BrickPi.MotorSpeed[motor2] = speed_left
  timer(no_seconds)

def fwd_amt(distance):
  global WHEELRADIUS, speed_left, speed_right
  speed_left = 204
  speed_right = 200
  circumference = 2 * math.pi * WHEELRADIUS
  print "Going forward "
  no_rotations = distance / circumference
  degrees  = no_rotations * 360
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right
  timer(10, adjustValues)
  
#Move Left
def left(no_seconds):
  print "Going left"
  global speed_left, speed_right
  speed_left = 80
  speed_right = -78
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right
  timer(no_seconds)
  
#Move backward
def back(no_seconds):
  global speed_left, speed_right
  print "Reversing"
  speed_left = -200 
  speed_right = -200
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right
  timer(no_seconds)
  
#Stop
def stop():
  print "- Stopping"
  BrickPi.MotorSpeed[motor1] = 0
  BrickPi.MotorSpeed[motor2] = 0

#Turn 90 degrees left
def left90deg():
  global no_seconds_left
  left(no_seconds_left)

#Timer
def timer(no_seconds):
  ot = time.time()
  while(time.time() - ot < no_seconds): # running while loop for no_seconds seconds
    BrickPiUpdateValues()            	# Ask BrickPi to update values for sensors/motors
    time.sleep(.01)                   	# sleep for 100 ms

def adjustValues():
  global speed_left, speed_right
  if BrickPi.E/leftncoder[motor1] > BrickPi.Encoder[motor2]:
    speed_left += 2
    return "left"
  elif BrickPi.Encoder[motor1] < BrickPi.Encoder[motor2]:
    speed_right += 2
    return "right"

for i in range(40):
  fwd(1)
  time.sleep(1)
  left90deg()
  time.sleep(0.5)
