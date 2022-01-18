#!/usr/bin/env python

import sys
import rospy
from std_msgs.msg import String
from pynput import keyboard
from pynput.keyboard import Key, Listener, KeyCode
import threading


class Teleop:
    def __init__(self, key_list, topic_name='key_press'):
        self.key_list = key_list    # Can't have "'" or ","        
        self.topic_name = topic_name
        
        self.pressed_key_list = []
        self.pub = rospy.Publisher(topic_name, String, queue_size=1)

        self.terminate = False
        threading.Thread(target=self.publish_thread).start()
        
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()


    def publish_thread(self):
        while not self.terminate:
            if self.pressed_key_list:
                msg = str(self.pressed_key_list)
                rospy.loginfo(msg)
                self.pub.publish(msg)

    def on_press(self, key):
        try:                
            if key.char in self.key_list:
                if key.char not in self.pressed_key_list:
                    self.pressed_key_list.append(str(key.char))

        except AttributeError:      
            if key in self.key_list:
                key_char = str(key).split('.')[1]
                if key_char not in self.pressed_key_list:  
                    self.pressed_key_list.append(key_char)   

    def on_release(self, key):
        if key == keyboard.Key.esc:
            self.terminate = True                
            return False    # Stop listener

        try:                
            if key.char in self.key_list:
                if key.char in self.pressed_key_list:
                    self.pressed_key_list.remove(key.char)

        except AttributeError:      
            if key in self.key_list:
                key_char = str(key).split('.')[1]
                if key_char in self.pressed_key_list:  
                    self.pressed_key_list.remove(key_char)
        
        if self.pressed_key_list:
            keyboard.Controller().press(self.pressed_key_list[0])


if __name__ == '__main__':
    try:
        rospy.init_node('teleop_node', anonymous=True)
        key_list = ['a', 'd', 's', 'w', Key.space]
        t = Teleop(key_list)
    except rospy.ROSInterruptException:
        pass
