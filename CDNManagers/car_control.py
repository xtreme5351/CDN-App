import math
import serial
from time import sleep
from random import randint

class CarControl:

    arduino_connected = False

    def __init__(self, _detector):
        self.detector = _detector

    def ControlSetup():
        try:
            arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)
            key = randint(0, 255)
            arduino.write(bytes(key, 'utf-8'))
            sleep(0.05)
            data =int(arduino.readline().decode('utf-8').rstrip())
            if(data == key):
                CarControl.arduino_connected = True
                print("Arduino handshake successful.")
            else:
                print("Arduino handshake failed.")
            #We need to include the port as one of the parameters that we use to set up the behaviour of the program and to call this function once from the calibration button.
        except:
            print("Issue with arduino connection.")

    def Steering(direction_angle, current_steering_lock):
        #Take in the angle the wheels should be and compare with the angle that they are at.
        #Send a command to the arduino to step the steering motor to the correct angle.
        
        #Get current_steering_lock from arduino
        turn_speed = 1
        turn_out = math.copysign(math.trunc((direction_angle - current_steering_lock)/turn_speed))*turn_speed

        if CarControl.arduino_connected:
            #Send command to arduino
            pass

    def Acceleration(distance):
        #Take in the distance to the following object (x) and input into a function to determine the throttle the car should have (a throttle of 0 is equivelant to braking while a low throttle could result in the car slowing - we need to determine how open the throttle needs to be to start the car moving).
        #The acceleration function should probably be: y = a - ae^(-x + b) {x >= -ln(1 - c) + b}; y = 0 {0 <= x < -ln(1 - c) + b}
        #where a is the maximum acceleration/throttle (best to be 1 so that we express everything as a percentage of full throttle), b is an offset for distance and c is the minimum throttle to get the car to move as a fraction of a).
        #Send a command to the arduino to alter the control signals to the motor control board depending on throttle responce y.

        max_throttle = 1
        agression = 1
        min_throttle = 0.5
        cutoff_distance = 2
        offset = cutoff_distance - math.log(1-min_throttle)
        if distance > cutoff_distance:
            throttle_out = max_throttle - max_throttle*math.e**(- agression * distance + offset)
        else:
            throttle_out = 0
        if CarControl.arduino_connected:
            #Send command to arduino
            pass
