import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)  # Method to identify pins
GPIO.setwarnings(False)

'''
Ena = 22
In1 = 27
In2 = 17
GPIO.setup(Ena, GPIO.OUT)
GPIO.setup(In1, GPIO.OUT)
GPIO.setup(In2, GPIO.OUT)
pwmA = GPIO.PWM(Ena, 100)
pwmA.start(0)

pwmA.ChangeDutyCycle(100)
GPIO.output(In1, GPIO.LOW)
GPIO.output(In2, GPIO.HIGH)
sleep(2)
GPIO.output(In1, GPIO.LOW)
GPIO.output(In2, GPIO.LOW)
pwmA.ChangeDutyCycle(0)
'''


class Motor:
    def __init__(self, EnaA, In1A, In2A, EnaB, In1B, In2B):
        # Declare pins
        # A = no tape side
        # B = tape side
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B
        # Delcare pins as outputs
        GPIO.setup(self.EnaA, GPIO.OUT)
        GPIO.setup(self.In1A, GPIO.OUT)
        GPIO.setup(self.In2A, GPIO.OUT)
        GPIO.setup(self.EnaB, GPIO.OUT)
        GPIO.setup(self.In1B, GPIO.OUT)
        GPIO.setup(self.In2B, GPIO.OUT)
        # Declare power and set initial speed to zero
        self.pwmA = GPIO.PWM(self.EnaA, 100)
        self.pwmA.start(0)
        self.pwmB = GPIO.PWM(self.EnaB, 100)
        self.pwmB.start(0)

    # Move
    def move(self, speed=0.5, turn=0, t=2):  # t = delay
        '''
        :param speed:
        :param turn:
        :param t:

        Speed from -1 to 1
        Turn from -1 to 1, with -1 being right and 1 being left
        Change Direction:
            In1A = HIGH, In2A = LOW --> CCW
            In1A = LOW, In2A = HIGH --> CW

            In1B = LOW, In2B = HIGH --> CCW
            In1B = HIGH, In2B = LOW --> CW
        '''

        # Restore values for ChangeDutyCycle function
        speed *= 100
        turn *= 100
        left_speed = speed + turn
        #print("left speed", left_speed)
        right_speed = speed - turn
        #print("right speed", right_speed)

        # Prevent speeds from being >100 or <-100
        if left_speed > 100:
            left_speed = 100
        elif left_speed < -100:
            left_speed = -100
        if right_speed > 100:
            right_speed = 100
        elif right_speed < -100:
            right_speed = -100

        # Change speed and make speeds positive
        self.pwmA.ChangeDutyCycle(abs(right_speed))
        self.pwmB.ChangeDutyCycle(abs(left_speed))

        # Change direction (CW vs CCW)
        # If > 0, turn CW. If < 0, turn CCW.
        if right_speed > 0:
            GPIO.output(self.In1A, GPIO.LOW)
            GPIO.output(self.In2A, GPIO.HIGH)
        else:
            GPIO.output(self.In1A, GPIO.HIGH)
            GPIO.output(self.In2A, GPIO.LOW)

        if left_speed > 0:
            GPIO.output(self.In1B, GPIO.LOW)
            GPIO.output(self.In2B, GPIO.HIGH)
        else:
            GPIO.output(self.In1B, GPIO.HIGH)
            GPIO.output(self.In2B, GPIO.LOW)

        sleep(t)

    # Stop motor
    def stop(self, t=0):
        # Side A
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        sleep(t)


def main():
    print("moving foward")
    motor1.move(.6, 2)
    print("stopping")
    motor1.stop(2)
    print("moving foward")
    motor1.move(.6, 2)
    print("stopping")
    motor1.stop(2)


if __name__ == '__main__':
    motor1 = Motor(22, 27, 17, 2, 3, 4)
    main()
