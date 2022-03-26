# test comment
from time import sleep

import numpy

from MotorModule import Motor
import KeyPressModule as kp
import JoyStickModule as js
from ObjDetectionModule import *
import threading
import socket
import pickle

# Values for object detection
THRESHOLD = 0.45
NMS = 0.2

# Motor and control settings
MOTOR = Motor(23, 3, 4, 22, 27, 17)
MOVEMENT = 'Joystick'  # Can use: [Keyboard, Joystick']

# Create lock global variable
my_lock = threading.Lock()

# Create obj detection info global variable
obj_det_info = []
box = []

# Initialize camera
cap = cv2.VideoCapture(0)
# Set width (3) and height (4)
cap.set(3, 640)
cap.set(4, 480)
# cap.set(10, 70)  # Brightness


def init_server():
    # Initialize remote video server
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)
    server_ip = "192.168.1.6"
    server_port = 6666
    return s, server_ip, server_port


def manual_motor_control():
    '''
    Control motors. Can use 'Joystick' or 'Keyboard' control.
    '''
    while True:
        if MOVEMENT == 'Joystick':
            # print(js.get_joystick())
            joystick_val = js.get_joystick()
            # LEFT JOYSTICK:  axis1 -> (left, right) // axis2 -> (up, down)
            # RIGHT JOYSTICK: axis3 -> (left, right) // axis4 --> (up, down)
            # motor.move(up/down, left/right, time in sec)
            MOTOR.move(-(joystick_val['axis4']), joystick_val['axis3'], .1)
            #print(joystick_val['axis4'])
            sleep(.05)

        else:
            # Initialize keyboard input
            kp.init()
            if kp.get_key('UP'):
                print('moving forward')
                MOTOR.move(.4, 0, .1)
            elif kp.get_key('DOWN'):
                print('moving backwards')
                MOTOR.move(-.4, 0, .1)
            elif kp.get_key('LEFT'):
                print('moving left')
                MOTOR.move(.5, -.8, .1)
            elif kp.get_key('RIGHT'):
                print('moving right')
                MOTOR.move(.5, .8, .1)
            else:
                MOTOR.stop(.1)


def send_to_server(s, server_ip, server_port):
    '''
    Stream video (without object detection) to server.
    :param success: bool (True if successful)
    :param img: image from video
    '''
    while True:
        #print('STREAM')
        # Lock cap.read() so only one function does this at a time
        my_lock.acquire()
        success, img = cap.read()
        my_lock.release()

        # Send image to be drawn on, and receive drawn image
        drawn_img = draw_on_img(img)

        # Send final image to server
        success, buffer = cv2.imencode(".jpg", drawn_img, [int(
            cv2.IMWRITE_JPEG_QUALITY), 30])
        x_as_bytes = pickle.dumps(buffer)
        s.sendto(x_as_bytes, (server_ip, server_port))


def draw_on_img(img):
    '''
    Draw name, box, and confidence level on image.
    :param img: current image to be drawn on
    :return: image with items drawn on
    '''
    # Will be updating global variable for box coordinates
    global box
    # For each object in the list (box, name, confidence), draw appropriately
    for current_obj in obj_det_info:
        for obj_info in current_obj:
            # Draw box
            if type(obj_info) == numpy.ndarray:
                box = obj_info
                cv2.rectangle(img, box, color=(180, 100, 200), thickness=4)
            # Draw object name
            elif type(obj_info) == str:
                cv2.putText(img, obj_info,
                            (box[0] + 10, box[1] + 30),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (180, 100, 200), 2)
                print(obj_info)
            # Draw confidence level
            else:
                cv2.putText(img, str(round(obj_info * 100, 2)), (box[0] + 10,
                                                                 box[1] + 75),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (180, 100, 200), 2)
    return img


def obj_detection():
    '''
    Object detection.
    '''
    #print('OBJ DET')
    while True:
        # Lock cap.read() so only one function does this at a time
        my_lock.acquire()
        success, img = cap.read()
        my_lock.release()

        # Can specify objects to detect using: objects=["person", "cup"]
        # Object info = 1 or 2D list of box coordinates, obj name, confidence
        result, object_info = get_objects(img, THRESHOLD, NMS, draw=True)

        #cv2.imshow('Webcam', result)

        # Update global variable of object info for a specific image
        global obj_det_info
        obj_det_info = object_info



def main():
    # Initialize server stream
    server_info = init_server()
    socket = server_info[0]
    server_ip = server_info[1]
    server_port = server_info[2]

    # Motor thread
    motor_thread = threading.Thread(target=manual_motor_control, args=())
    motor_thread.start()

    # Server video thread
    server_thread = threading.Thread(target=send_to_server, args=(socket,
                                                                  server_ip,
                                                                  server_port))
    server_thread.start()

    # Object detection thread
    obj_det_thread = threading.Thread(target=obj_detection, args=())
    obj_det_thread.start()

    # Press enter to quit
    if cv2.waitKey(1) == 13:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()