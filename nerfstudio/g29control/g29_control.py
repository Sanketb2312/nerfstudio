#!/home/sanket/anaconda3/envs/nerfstudio/bin/python


import sys
import pip
import rospy
from sensor_msgs.msg import Joy
from socket import *
from codecs import decode
import requests
#import keyboard
#from pynput import keyboard
print(sys.executable)

#pip.main(["install", "pynput"])

import keyboard


import pynput
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

# Initialize pygame for joystick input

# url = "http://0.0.0.0:7007/"

# response = requests.get(url)

# if response.status_code == 200:
#     print("Request successful!")
#     print("Response content:")
#     print(response.text)
# else:
#     print(f"Error: {response.status_code}")



#global variables for G29 steeringwheel
joy_publisher = rospy.Publisher('joy', Joy, queue_size=1)

# Create a Joy message
joy_msg = Joy()

#auto_orient_and_center_poses
#viewmatrix
steering  = None
break_pedal = None
acceleration_pedal = None
sqaure = None
triangle = None
circle = None
x = None
left = None
right = None
accelerator_pressed = False


def joy_callback(data):
    global accelerator_pressed
    print("Received Joy message:")
    print("Header:", data.header)
    print("Axes:", data.axes)
    print("Buttons:", data.buttons)
    print("---")

    print("Steering: ", data.axes[0])
    print("Break: ", data.axes[3])
    print("Acceleration: ", data.axes[2])
    print("button: ", data.buttons[2])



    steering = data.axes[0]
    break_pedal = data.axes[3]
    acceleration_pedal = data.axes[2]
    sqaure = data.buttons[1]
    triangle = data.buttons[3]
    circle = data.buttons[2]
    x = data.buttons[0]
    side_movement = data.axes[4]
    right = data.axes[5]

    if acceleration_pedal > -1:
        keyboard.press('w')
        accelerator_pressed = True

        # Sleep for 1ms
        #time.sleep(0.001)

        # Release 'w'
        #keyboard.release('w')
        accelerator_pressed = False

    if accelerator_pressed:
        # Fully release 'w'
        keyboard.release('w')
        accelerator_pressed = False

    mapping(sqaure, triangle, circle, x, steering, acceleration_pedal, break_pedal, side_movement)



def mapping(sqaure, triangle, circle, x, steering, acceleration_pedal, break_pedal, side_movement):
    prev_time = time.localtime().tm_sec
    if acceleration_pedal > -1:
        keyboard.press('w')
        #accelerator_pressed = True

        # Sleep for 1ms
        #time.sleep(0.001)

        # Release 'w'
        keyboard.release('w')
        #accelerator_pressed = False

    # if accelerator_pressed:
    #     # Fully release 'w'
    #     keyboard.release('w')
    #     accelerator_pressed = False

    if steering > 0.025:
        keyboard.press('a')
        keyboard.press(Key.right)
    
    if -0.025 < steering < 0.025:
        keyboard.release('a')
        keyboard.release('d')
        keyboard.release(Key.right)
        keyboard.release(Key.left)

    if steering < -0.025:
        keyboard.press('d')
        keyboard.press(Key.left)
    
    if side_movement == -1:
        keyboard.press('a')
    
    if side_movement == 1:
        keyboard.press('d')

    if side_movement == 0:
        keyboard.release('a')
        keyboard.release('d')


    #triangle == 1:
    #     keyboard.press('a')

    # elif triangle == 0:
    #     keyboard.release('a')
    
    # if circle == 1:
    #     keyboard.press('d')

    # elif circle == 0:
    #     keyboard.release('d')

    # if x == 1:
    #     keyboard.press('s')
    # if x == 0:
    #     keyboard.release('s')
    







def main():

    rospy.init_node('g29_button_mapping')

    rospy.Subscriber('joy', Joy, joy_callback)
    # Keep the script running
    rospy.spin()



if __name__ == "__main__":
    main()
