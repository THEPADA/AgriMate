#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from pynput import keyboard
from pynput.keyboard import Key, Listener
import sys

def talker(my_msg):
    rospy.loginfo(my_msg)
    pub.publish(my_msg)

def on_press(key):
    global pressed
    global selected_key
    if selected_key == Key.esc:
        selected_key = key
        print("Listening to {0}".format(key))
    elif key == selected_key and pressed == False:
        pressed = True
        my_msg = "pressed {0} key".format(key)
        talker(my_msg)

def on_release(key):
    global pressed
    if pressed == True:
        if key == selected_key or key == Key.esc:
            pressed = False
            my_msg = "released {0} key".format(key)
            talker(my_msg)
    if key == Key.esc:
        return False

if __name__ == '__main__':
    if sys.argv[1] == None:
        print("add name for publisher as an argument")
        sys.exit()
    try:
        pressed = False
        selected_key = Key.esc
        print("Press esc to exit")
        print("Publishes selected key press and release")
        print("press any key to start listening")
        pub = rospy.Publisher('chatter', String, queue_size=10)
        rospy.init_node(sys.argv[1], anonymous=True)
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except rospy.ROSInterruptException:
        pass
