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
#from numpy import mean
import random
import datetime
import math, sys
from collections import Counter

#Setting up BrickPi
BrickPiSetup()  

motor1 = PORT_A
motor2 = PORT_B
motorASpeed = 250 
motorBSpeed = 250

#Enabling the motors:
BrickPi.MotorEnable[motor1] = 1 
BrickPi.MotorEnable[motor2] = 1 

# Reset the motor sensor reading
BrickPi.Encoder[motor1] = 0
BrickPi.Encoder[motor2] = 0

DISTANCE = PORT_3
#BrickPi.SensorType[PORT_1] = TYPE_SENSOR_TOUCH
#BrickPi.SensorType[PORT_2] = TYPE_SENSOR_TOUCH
#BrickPi.SensorType[PORT_3] = TYPE_SENSOR_TOUCH
#BrickPi.SensorType[PORT_4] = TYPE_SENSOR_TOUCH
BrickPi.SensorType[DISTANCE] = TYPE_SENSOR_ULTRASONIC_CONT


BrickPiSetupSensors()   

#Radius of our wheel (subject to calibration)
WHEEL_AXLE = 2.2

#Default speeds (subject to calibration)
DEFAULT_MOTOR_A_SPEED = 250
DEFAULT_MOTOR_B_SPEED = 250
DEFAULT_TARGET_SPEED = 202
DEFAULT_DISTANCE = 45
CURRENT_DISTANCE = 45
DEFAULT_CORNER_SPEED = 65 

#Moving Forward
def forward(distance):
  global WHEEL_AXLE, motorASpeed, motorBSpeed
  BrickPiUpdateValues()
  encoder_1 = BrickPi.Encoder[motor1]
  encoder_2 = BrickPi.Encoder[motor2]
  #motorASpeed = DEFAULT_MOTOR_A_SPEED
  #motorBSpeed = DEFAULT_MOTOR_B_SPEED
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
    
def forwardCorner(distance, factor):
  global WHEEL_AXLE, motorASpeed, motorBSpeed
  BrickPiUpdateValues()
  encoder_1 = BrickPi.Encoder[motor1]
  encoder_2 = BrickPi.Encoder[motor2]
  motorASpeed = DEFAULT_CORNER_SPEED
  motorBSpeed = DEFAULT_CORNER_SPEED
  circumference = 2 * math.pi * WHEEL_AXLE
  print "Going forwards"
  no_rotations = distance / circumference
  degrees  = no_rotations * 720
  BrickPi.MotorSpeed[motor1] = motorASpeed
  BrickPi.MotorSpeed[motor2] = motorBSpeed
  while(BrickPi.Encoder[motor1] - encoder_1 < degrees
    and BrickPi.Encoder[motor2] - encoder_2 < degrees):
    BrickPiUpdateValues()
    calibrateCorner(degrees, encoder_1, encoder_2, factor)
    time.sleep(.001)

def calibrate(degrees, encoder_1, encoder_2):
  global motorASpeed, motorBSpeed
  rotationsA = BrickPi.Encoder[motor1] - encoder_1
  rotationsB = BrickPi.Encoder[motor2] - encoder_2
  target_speed = motorASpeed#DEFAULT_TARGET_SPEED
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
  #print 'calibrating:', motorASpeed, motorBSpeed
  BrickPi.MotorSpeed[motor1] = motorASpeed
  BrickPi.MotorSpeed[motor2] = motorBSpeed

def calibrateCorner(degrees, encoder_1, encoder_2, factor):
  global motorASpeed, motorBSpeed
  rotationsA = BrickPi.Encoder[motor1] - encoder_1
  rotationsB = BrickPi.Encoder[motor2] - encoder_2
  target_speed = DEFAULT_CORNER_SPEED
  speed1 = BrickPi.MotorSpeed[motor1]
  speed2 = BrickPi.MotorSpeed[motor2]
  #Coeficient (found by calibrating)
  k = factor
  delta = 30 - CURRENT_DISTANCE
  print "dist: ",CURRENT_DISTANCE
  if (delta==0):
     return
  change = float(1)/delta
  if 30 > CURRENT_DISTANCE:
    print "close: ", abs(int(k*(1-change)))
    motorASpeed = target_speed + abs(int(k * (1 - change)))
    motorBSpeed = target_speed - abs(int(k * (1 - change)))
  elif 30 < CURRENT_DISTANCE:
    print "away: ", abs(int(k*(1+change)))
    motorASpeed = target_speed - abs(int(k * (1 + change)))
    motorBSpeed = target_speed + abs(int(k * (1 + change)))
  print "diff", delta
  print "A:", motorASpeed, "\tB:", motorBSpeed
  BrickPi.MotorSpeed[motor1] = min(target_speed+30,max(40,motorASpeed))
  BrickPi.MotorSpeed[motor2] = min(target_speed+30,max(40,motorBSpeed+3))

#Move backward
def move_backwards(distance):
  global WHEEL_AXLE, motorASpeed, motorBSpeed
  BrickPiUpdateValues()
  encoder_1 = BrickPi.Encoder[motor1]
  encoder_2 = BrickPi.Encoder[motor2]
  motorASpeed = -abs(motorASpeed)
  motorBSpeed = -abs(motorBSpeed)
  circumference = 2 * math.pi * WHEEL_AXLE
  print "Going backwards"
  no_rotations = distance / circumference
  degrees  = no_rotations * 720
  BrickPi.MotorSpeed[motor1] = motorASpeed
  BrickPi.MotorSpeed[motor2] = motorBSpeed
  print "going in loop"
  while(encoder_1 - BrickPi.Encoder[motor1] < degrees
    and encoder_2 - BrickPi.Encoder[motor2] < degrees): 
    BrickPiUpdateValues()            	
    calibrateBack(degrees, encoder_1, encoder_2) 
    time.sleep(.001)                   	

def calibrateForward(degrees, encoder_1, encoder_2):
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

    
def calibrateBack(degrees, encoder_1, encoder_2):
  global motorASpeed, motorBSpeed
  rotationsA = BrickPi.Encoder[motor1] - encoder_1
  rotationsB = BrickPi.Encoder[motor2] - encoder_2
  target_speed = -abs(motorASpeed)
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
def wait(duration):
  print "Sleep...zzzz"
  BrickPi.MotorSpeed[motor1] = 0
  BrickPi.MotorSpeed[motor2] = 0
  BrickPiUpdateValues()
  time.sleep(duration)

#Turn -- private function
def turn(deg, orientation):
  global WHEEL_AXLE, motorASpeed, motorBSpeed

  print "Rotating Left"
  if orientation == 'r':
    motorASpeed = -DEFAULT_MOTOR_A_SPEED
    motorBSpeed = DEFAULT_MOTOR_B_SPEED
  elif orientation == 'l':
    motorASpeed = DEFAULT_MOTOR_A_SPEED
    motorBSpeed = -DEFAULT_MOTOR_A_SPEED
  else:
    return 
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

def nonpseudorandom():
  random_seed = datetime.datetime.now().time().microsecond
  random.seed(random_seed)
  if random.random() <= 0.5:
    return True
  return False  

def run():
  while True:
    forward(10)
    result = BrickPiUpdateValues()
    if not result:
      left = BrickPi.Sensor[PORT_4]
      right = BrickPi.Sensor[PORT_1]
      if left==1 and right==1:
        bump(1)
      elif left==1:
        bump(2)
      elif right==1:
        bump(3)
    time.sleep(0.001)

def cont_distance():
  i = 0
  while(i<10):
    print get_distance()
    i+=1
  

def get_distance():
  global CURRENT_DISTANCE
  values = []
  result = BrickPiUpdateValues()
  #for i in range(100):
  #  BrickPiUpdateValues()
  for i in range(10):
    result = BrickPiUpdateValues()
    if not result:
      distance = BrickPi.Sensor[DISTANCE]
      values.append(distance)
  #values.sort()
  #for i in range(9):
  #  if values[i+1] - values[i] >= 128:
  #    values[i+1] -= 128
  values.sort()
  print values
  readings = Counter(values)
  mode = readings.most_common(1)[0][0]
  
  return mode#values[len(values)/2]

def max(a, b):
  if a > b:
    return a
  return b

def require_distance():
  global motorASpeed, motorBSpeed
  BrickPiUpdateValues()
  actual_distance = get_distance()
  print "distance", actual_distance
  going_forwards = True  
  while True:
    print "distance", actual_distance
    actual_distance = get_distance()
    diff = actual_distance - DEFAULT_DISTANCE
    if (abs(diff) <3):
      wait(0.1)
      continue
    delta = float(1) / diff
    print 'delta:', delta
    if delta>=0:
        if not going_forwards:
           wait(0.1)
           going_forwards = True
        k = 1 - delta
        motorASpeed = max(50, int(k*250))
        motorBSpeed = max(50, int(k*250))
        forward(1)
    else:
        k = 1 + delta
        if going_forwards:
           wait(0.1)
           going_forwards = False
        print "I think I'll crash"
	motorASpeed = max(50, int(k*250))
        motorBSpeed = max(50, int(k*250))
        move_backwards(1)
    print 'k:', k
    #motorASpeed = 0
    #motorBSpeed = 0
    print 'motorASpeed:', motorASpeed
    print 'motorBSpeed:', motorBSpeed
    #forward(1)
    #actual_distance = get_distance()
    time.sleep(0.01)
  #wait(1)

def run_corner(factor):
  global CURRENT_DISTANCE
  BrickPi.MotorSpeed[motor1] = DEFAULT_CORNER_SPEED
  BrickPi.MotorSpeed[motor1] = DEFAULT_CORNER_SPEED
  while True:    
    result = BrickPiUpdateValues()
    if not result:
      distance = get_distance()
      CURRENT_DISTANCE = distance
      print "distance: ", distance
    forwardCorner(0.5, factor)
    time.sleep(0.01)

def bump(hit_val):
   print "bump(", hit_val, ")"
   print "in back"
   print "hit val=", hit_val
   wait(0.1)
   move_backwards(10)
   print "going in if"
   if hit_val==1:
     print "val being 1"
     if nonpseudorandom():
       turn(90, 'l')
     else:
       turn(90, 'r')
   elif hit_val==2:
     print "Val being 2"
     turn(90,'l')
   elif hit_val==3:
     print "val being 3"
     turn(90,'r') 

def main():
  print "Begining sensor testing"
  #BrickPi.SensorType[PORT_1] = TYPE_SENSOR_TOUCH
  #BrickPi.SensorType[PORT_2] = TYPE_SENSOR_TOUCH
  #BrickPi.SensorType[PORT_3] = TYPE_SENSOR_TOUCH
  #BrickPi.SensorType[PORT_4] = TYPE_SENSOR_TOUCH
  #move_backwards(10)
  #run()
  #require_distance()
  while True:
    cont_distance()
  #run_corner(10)
main()

