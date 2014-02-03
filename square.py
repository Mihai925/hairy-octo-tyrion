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
import math, sys

WHEELRADIUS = 2.2  # Lego wheel radius

BrickPiSetup()  # setup the serial port for communication

motor1 = PORT_A
motor2 = PORT_B
speed_left = 0 
speed_right = 0

BrickPi.MotorEnable[motor1] = 1 #Enable the Motor A
BrickPi.MotorEnable[motor2] = 1 #Enable the Motor B

# Reset the motor sensor reading
BrickPi.Encoder[motor1] = 0
BrickPi.Encoder[motor2] = 0

BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

#Move Forward
def forward(distance):
  global WHEELRADIUS, speed_left, speed_right
  BrickPiUpdateValues()
  offset_1 = BrickPi.Encoder[motor1]
  offset_2 = BrickPi.Encoder[motor2]
  speed_left = 200
  speed_right = 204
  circumference = 2 * math.pi * WHEELRADIUS
  print "Going forward"
  no_rotations = distance / circumference
  degrees  = no_rotations * 720
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right
  while(BrickPi.Encoder[motor1] - offset_1 < degrees
    and BrickPi.Encoder[motor2] - offset_2 < degrees): # running while loop for no_seconds seconds
    BrickPiUpdateValues()            	# Ask BrickPi to update values for sensors/motors
    adjustValues(degrees, offset_1, offset_2)
    time.sleep(.001)                   	# sleep for 100 ms
    
def adjustValues(degrees, offset_1, offset_2):
  global speed_left, speed_right
  rot1 = BrickPi.Encoder[motor1] - offset_1
  rot2 = BrickPi.Encoder[motor2] - offset_2
  target_speed = 202
  k = 1 # coefficient
  if rot1 < rot2:
    diff = rot2 - rot1
    speed_left = target_speed + diff * k
    speed_right = target_speed - diff * k
  elif rot1 > rot2: 
    diff = rot1 - rot2
    speed_left = target_speed - diff * k
    speed_right = target_speed + diff * k
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right

#Move backward
def back(distance):
  global WHEELRADIUS, speed_left, speed_right
  BrickPiUpdateValues()
  offset_1 = BrickPi.Encoder[motor1]
  offset_2 = BrickPi.Encoder[motor2]
  speed_left = -200
  speed_right = -204
  circumference = 2 * math.pi * WHEELRADIUS
  print "Going backward"
  no_rotations = distance / circumference
  degrees  = no_rotations * 720
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right
  while(offset_1 - BrickPi.Encoder[motor1] < degrees
    and offset_2 - BrickPi.Encoder[motor2] < degrees): 
    BrickPiUpdateValues()            	# Ask BrickPi to update values for sensors/motors
    adjustValuesBack(degrees, offset_1, offset_2) # Automatic speeds adjustment
    time.sleep(.001)                   	# Sleep for 100 ms
    
def adjustValuesBack(degrees, offset_1, offset_2):
  global speed_left, speed_right
  spins1 = BrickPi.Encoder[motor1] - offset_1
  spins2 = BrickPi.Encoder[motor2] - offset_2
  target_speed = -202
  k = 1 # coefficient
  if spins1 < spins2:
    diff = spins2 - spins1
    speed_left = target_speed + diff * k
    speed_right = target_speed - diff * k
  elif spins1 > spins2: 
    diff = spins1 - spins2
    speed_left = target_speed - diff * k
    speed_right = target_speed + diff * k
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right

#wait
def wait():
  print "Waiting"
  BrickPi.MotorSpeed[motor1] = 0
  BrickPi.MotorSpeed[motor2] = 0
  BrickPiUpdateValues()
  time.sleep(0.5)

#Turn -- private function
def turn(deg, orientation):
  global WHEELRADIUS, speed_left, speed_right
  
  #Adjust initial speeds
  if (orientation == "l"):
    print "Turning Left"
    speed_left = -200
    speed_right = 204 
  elif (orientation == "r"):
    print "Turning Right"
    speed_left = 200
    speed_right = -204
  else:
    raise Exception("undefined orientation")

  #Establish number of spins
  axle = 6.0
  distance = axle * 2 * math.pi * deg / 360 
  circumference = 2 * math.pi * WHEELRADIUS
  no_rotations = distance / circumference
  degrees  = no_rotations * 720 
  
  BrickPiUpdateValues()
  offset_1 = BrickPi.Encoder[motor1]
  offset_2 = BrickPi.Encoder[motor2]

  #Start turning 
  BrickPi.MotorSpeed[motor1] = speed_left
  BrickPi.MotorSpeed[motor2] = speed_right
 
  while(abs(BrickPi.Encoder[motor1] - offset_1) < degrees
    and abs(BrickPi.Encoder[motor2] - offset_2) < degrees): 
    BrickPiUpdateValues()
    time.sleep(.001)

def main():
  size = 30
  print "Starting Robot"
  for i in range(4):
      forward(float(size))
      wait()
      turn(90, "l")
      wait()
  print "End"


main()