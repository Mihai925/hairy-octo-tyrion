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

# Authors: Mihai Jiplea, Critina Budurean, Rohan Mahtani, Varun Verma

#Importing the BrickPi library 
from BrickPi import *  
import math, sys


#Setting up BrickPi
BrickPiSetup()  

motor1 = PORT_A
motor2 = PORT_B
motorASpeed = 0 
motorBSpeed = 0

#Enabling the motors:
BrickPi.MotorEnable[motor1] = 1 
BrickPi.MotorEnable[motor2] = 1 

# Reset the motor sensor reading
BrickPi.Encoder[motor1] = 0
BrickPi.Encoder[motor2] = 0

BrickPiSetupSensors()   

#Radius of our wheel (subject to calibration)
WHEEL_AXLE = 2.2

#Default speeds (subject to calibration)
DEFAULT_MOTOR_A_SPEED = 200
DEFAULT_MOTOR_B_SPEED = 204
DEFAULT_TARGET_SPEED = 202

#Moving Forward
def forward(distance):
  global WHEEL_AXLE, motorASpeed, motorBSpeed
  BrickPiUpdateValues()
  encoder_1 = BrickPi.Encoder[motor1]
  encoder_2 = BrickPi.Encoder[motor2]
  motorASpeed = DEFAULT_MOTOR_A_SPEED
  motorBSpeed = DEFAULT_MOTOR_B_SPEED
  circumference = 2 * math.pi * WHEEL_AXLE
  print "Going forwards"
  no_rotations = distance / circumference
  degrees  = no_rotations * 720
  BrickPi.MotorSpeed[motor1] = motorASpeed
  BrickPi.MotorSpeed[motor2] = motorBSpeed
  while(BrickPi.Encoder[motor1] - encoder_1 < degrees
    and BrickPi.Encoder[motor2] - encoder_2 < degrees): 
    BrickPiUpdateValues()            	
    calibrate(degrees, encoder_1, encoder_2)
    time.sleep(.001)                   	
    
def calibrate(degrees, encoder_1, encoder_2):
  global motorASpeed, motorBSpeed
  rotationsA = BrickPi.Encoder[motor1] - encoder_1
  rotationsB = BrickPi.Encoder[motor2] - encoder_2
  target_speed = DEFAULT_TARGET_SPEED
  #Coeficient (found by calibrating)
  k = 1 
  if rotationsA < rotationsB:
    diff = rotationsB - rotationsA
    motorASpeed = target_speed + diff * k
    motorBSpeed = target_speed - diff * k
  elif rotationsA > rotationsB: 
    diff = rotationsA - rotationsB
    motorASpeed = target_speed - diff * k
    motorBSpeed = target_speed + diff * k
  BrickPi.MotorSpeed[motor1] = motorASpeed
  BrickPi.MotorSpeed[motor2] = motorBSpeed

#Move backward
def move_backwards(distance):
  global WHEEL_AXLE, motorASpeed, motorBSpeed
  BrickPiUpdateValues()
  encoder_1 = BrickPi.Encoder[motor1]
  encoder_2 = BrickPi.Encoder[motor2]
  motorASpeed = -DEFAULT_MOTOR_A_SPEED
  motorBSpeed = -DEFAULT_MOTOR_B_SPEED
  circumference = 2 * math.pi * WHEEL_AXLE
  print "Going backwards"
  no_rotations = distance / circumference
  degrees  = no_rotations * 720
  BrickPi.MotorSpeed[motor1] = motorASpeed
  BrickPi.MotorSpeed[motor2] = motorBSpeed
  while(encoder_1 - BrickPi.Encoder[motor1] < degrees
    and encoder_2 - BrickPi.Encoder[motor2] < degrees): 
    BrickPiUpdateValues()            	
    calibrateBack(degrees, encoder_1, encoder_2) 
    time.sleep(.001)                   	
    
def calibrateBack(degrees, encoder_1, encoder_2):
  global motorASpeed, motorBSpeed
  rotationsA = BrickPi.Encoder[motor1] - encoder_1
  rotationsB = BrickPi.Encoder[motor2] - encoder_2
  target_speed = -DEFAULT_TARGET_SPEED
  #Coeficient (found by calibrating)
  k = 1 
  if rotationsA < rotationsB:
    diff = rotationsB - rotationsA
    motorASpeed = target_speed + diff * k
    motorBSpeed = target_speed - diff * k
  elif rotationsA > rotationsB: 
    diff = rotationsA - rotationsB
    motorASpeed = target_speed - diff * k
    motorBSpeed = target_speed + diff * k
  BrickPi.MotorSpeed[motor1] = motorASpeed
  BrickPi.MotorSpeed[motor2] = motorBSpeed

#Waiting
def wait():
  print "Sleep...zzzz"
  BrickPi.MotorSpeed[motor1] = 0
  BrickPi.MotorSpeed[motor2] = 0
  BrickPiUpdateValues()
  time.sleep(0.5)

#Turn -- private function
def turn(deg):
  global WHEEL_AXLE, motorASpeed, motorBSpeed

  print "Rotating Left"
  motorASpeed = -DEFAULT_MOTOR_A_SPEED
  motorBSpeed = DEFAULT_MOTOR_B_SPEED 
  #Establish number of spins
  axle = 6.0
  distance = axle * 2 * math.pi * deg / 360 
  circumference = 2 * math.pi * WHEEL_AXLE
  no_rotations = distance / circumference
  degrees  = no_rotations * 720 
  
  BrickPiUpdateValues()
  encoder_1 = BrickPi.Encoder[motor1]
  encoder_2 = BrickPi.Encoder[motor2]

  #Start turning 
  BrickPi.MotorSpeed[motor1] = motorASpeed
  BrickPi.MotorSpeed[motor2] = motorBSpeed
 
  while(abs(BrickPi.Encoder[motor1] - encoder_1) < degrees
    and abs(BrickPi.Encoder[motor2] - encoder_2) < degrees): 
    BrickPiUpdateValues()
    time.sleep(.001)

def main():
  size = 30
  print "Begining square program"
  for i in range(4):
      forward(float(size))
      wait()
      turn(90)
      wait()
  print "Square ended"

main()
