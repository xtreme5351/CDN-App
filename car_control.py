def Steer(direction_angle, current_steering_lock):
    pass
    #Take in the angle the wheels should be and compare with the angle that they are at.
    #Send a command to the arduino to step the steering motor to the correct angle.

def Acceleration(distance):
    pass
    #Take in the distance to the following object (x) and input into a function to determine the throttle the car should have (a throttle of 0 is equivelant to braking while a low throttle could result in the car slowing - we need to determine how open the throttle needs to be to start the car moving).
    #The acceleration function should probably be: y = a - ae^(-x + b) {x >= -ln(1 - c) + b}; y = 0 {0 <= x < -ln(1 - c) + b}
    #where a is the maximum acceleration/throttle (best to be 1 so that we express everything as a percentage of full throttle), b is an offset for distance and c is the minimum throttle to get the car to move as a fraction of a).
    #Send a command to the arduino to alter the control signals to the motor control board depending on throttle responce y