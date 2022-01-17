#!/usr/bin/env python

import sys
import rospy
from std_msgs.msg import String
from pynput import keyboard
from pynput.keyboard import Key, Listener, KeyCode

class Teleop:
    def __init__(self, key_list, topic_name='key_press'):
        self.key_list = key_list        
        self.topic_name = topic_name
        
        self.pressed_key_list = []
        self.pub = rospy.Publisher(topic_name, String, queue_size=1)

        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        msg = '{0}_p'.format(key)
        try:
            if key.char in self.key_list:
                if key.char not in self.pressed_key_list:
                    self.pressed_key_list.append(key.char)                
                    self.publish(msg)
        
        except AttributeError:
            if key in self.key_list:
                if key.char not in self.pressed_key_list:
                    self.pressed_key_list.append(key)                
                    self.publish(msg)


    def on_release(self, key):
        msg = '{0}_r'.format(key)
        try:
            if key.char in self.key_list:
                self.pressed_key_list.remove(key.char)
                self.publish(msg)
        
        except AttributeError:
            if key == keyboard.Key.esc:                
                return False    # Stop listener
            if key in self.key_list:
                self.pressed_key_list.remove(key)
                self.publish(msg)
    
    def publish(self, msg):
        rospy.loginfo(msg)
        self.pub.publish(msg)
        

if __name__ == '__main__':
    try:
        rospy.init_node('teleop_node', anonymous=True)
        key_list = ['a', 'd', 's', 'w', Key.space]
        t = Teleop(key_list)
    except rospy.ROSInterruptException:
        pass

