## CW 1 code
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

BrickPiSetup()  # setup the serial port for communication

motor1 = PORT_A
motor2 = PORT_B #red sticker
rotateTime = 1.2
rotateSpeed = 140

BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
BrickPi.MotorEnable[PORT_B] = 1 #Enable the Motor B
#BrickPiStruct = BrickPiStruct()
Motor1Speed = 140
Motor2Speed = 140
GoingForward = None
BrickPiSetupSensors()   #Send the properties of sensors to BrickPi

def rotateRight():
        print "Rotating Right"
        BrickPi.MotorSpeed[motor1] = -rotateSpeed
        BrickPi.MotorSpeed[motor2] = rotateSpeed
        ot = time.time()
        while(time.time() - ot < rotateTime):
                BrickPiUpdateValues()
                time.sleep(.1)

def rotateLeft():
	print "Rotating Left"
	BrickPi.MotorSpeed[motor1] = rotateSpeed-11
	BrickPi.MotorSpeed[motor2] = -rotateSpeed
	ot = time.time()
	while(time.time() -ot < rotateTime):
		BrickPiUpdateValues()
		time.sleep(.1)	

def forward40():
	global GoingForward
	global Motor1Speed
	global Motor2Speed
	Motor1Speed = -Motor1Speed
	Motor2Speed = -Motor2Speed
	GoingForward = True
	print "Running Forward"
	BrickPi.MotorSpeed[motor1] = Motor1Speed
	BrickPi.MotorSpeed[motor2] = Motor2Speed
	ot = time.time()
	while(time.time() - ot < 2):
		#BrickPiUpdateValues()
		calibrate()
		print BrickPi.MotorSpeed[motor1], BrickPi.MotorSpeed[motor2]
		time.sleep(.1)

def backward40():
	global GoingForward
	global Motor1Speed
	global Motor2Speed
	Motor1Speed = abs(Motor1Speed)
	Motor2Speed = abs(Motor2Speed)
	GoingForward = False
        print "Running Backward"
        BrickPi.MotorSpeed[motor1] = Motor1Speed
        BrickPi.MotorSpeed[motor2] = Motor2Speed
        ot = time.time()
        while(time.time() - ot < 2):
                #BrickPiUpdateValues()
		calibrate()
		print BrickPi.MotorSpeed[motor1], BrickPi.MotorSpeed[motor2]
                time.sleep(.1)


def randomMove():
	while True:
		forward40()
		backward40()
#		rotateRight()
#		forward40()
#		rotateLeft()
#		forward40()
#        	rotateLeft()
#		forward40()
#		rotateLeft()
#		forward40()

def square():
	forward40()
	time.sleep(0.1)
	rotateRight()
	time.sleep(0.1)
	forward40()
	time.sleep(0.1)
	rotateRight()
	time.sleep(0.1)
	forward40()
	time.sleep(0.1)
	rotateRight()
	time.sleep(0.1)
	forward40()
	time.sleep(0.1)
	rotateRight()
	time.sleep(0.1)

def calibrate():
	global Motor1Speed
	global Motor2Speed
	global GoingForward
	Motor1RotT1 = BrickPi.Encoder[PORT_A]
	Motor2RotT1 = BrickPi.Encoder[PORT_B]
	BrickPiUpdateValues()
	Motor1RotT2 = BrickPi.Encoder[PORT_A]
	Motor2RotT2 = BrickPi.Encoder[PORT_B]
	Motor1Rot = Motor1RotT2 - Motor1RotT1
	Motor2Rot = Motor2RotT2 - Motor2RotT1
	
	i = 3	
	if Motor1Rot > Motor2Rot:
		#Motor1Speed = BrickPi.MotorSpeed[motor1]
		Motor1Speed -= i
		BrickPi.MotorSpeed[motor1] = Motor1Speed
	elif Motor1Rot < Motor2Rot:
		Motor1Speed += i
		BrickPi.MotorSpeed[motor2] = Motor2Speed
	#BrickPiUpdateValues()

#square()
#randomMove()
#while True:
	#forward40()
	#backward40()

#while True:
#circle()
#rotateLeft()


#rotateRight()
#time.sleep(0.2)
#rotateRight()
#time.sleep(0.2)
#rotateLeft()
#time.sleep(0.2)
#rotateRight()
#time.sleep(0.2)
#	rotateLeft()



def main():
	BrickPiUpdateValues()
	randomMove()
	pass

#print dir(BrickPi)	
main()

