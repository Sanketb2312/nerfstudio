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
import subprocess
import evdev
print(sys.executable)

#pip.main(["install", "pynput"])
from nerfstudio.utils.scripts import run_command
from nerfstudio.process_data.metashape_utils import metashape_to_json
from nerfstudio.cameras.camera_paths import get_interpolated_camera_path
from nerfstudio.cameras.camera_utils import auto_orient_and_center_poses, viewmatrix
from nerfstudio.viewer.viewer_elements import ViewerClick
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


def joy_callback(data):
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
    mapping(sqaure, triangle, circle, x, steering, acceleration_pedal, break_pedal)



def mapping(sqaure, triangle, circle, x, steering, acceleration_pedal, break_pedal):
    while acceleration_pedal > -1:
        if acceleration_pedal == -1:
            keyboard.release('w')
            break
        keyboard.press('w')
        time.sleep(0.2)

    if triangle == 1:
        keyboard.press('a')

    elif triangle == 0:
        keyboard.release('a')
    
    if circle == 1:
        keyboard.press('d')

    elif circle == 0:
        keyboard.release('d')

    if x == 1:
        keyboard.press('s')
    if x == 0:
        keyboard.release('s')
    







def main():

    rospy.init_node('g29_button_mapping')

    rospy.Subscriber('joy', Joy, joy_callback)
    # Keep the script running
    rospy.spin()



if __name__ == "__main__":
    main()
