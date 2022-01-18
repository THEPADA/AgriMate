#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825
from std_msgs.msg import String

class WASDController:
	def __init__(self, key_list, topic_name='key_press'):
        self.topic_name = topic_name
        self.u = 0.1
		self.v = 0.2

		self.sub = rospy.Subscriber(
           topic_name, String, self.motor_callback)

		self.motor_l = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
		self.motor_l.SetMicroStep('hardward' ,'fullstep')
		
		self.motor_r = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
		self.motor_r.SetMicroStep('hardward' ,'fullstep')

		self.v_l = 0
		self.v_r = 0
		
		# Motor2.TurnStep(Dir='forward', steps=6400, stepdelay=0.000001)

	def motor_callback(data):

		key, mode = data.split('_'):

		if mode == 'p':
			sign = 1
		else:
			sign == -1

		if key == 'w':
			self.v_l += sign*self.v
			self.v_r += sign*self.v

		if key == 's':
			self.v_l -= sign*self.v
			self.v_r -= sign*self.v

		if key == 'a':
			self.v_l -= sign*self.u
			self.v_r += sign*self.u

		if key == 'd':
			self.v_l += sign*self.u
			self.v_r -= sign*self.u

		# todo: send command to spin motors using v_l and v_r
		if(self.v_l < 0):
			dir_l = 'backward'
		else:
			dir_l = 'forward'
		if(self.v_r < 0):
			dir_r = 'backward'
		else:
			dir_r = 'forward'

		self.motor_l.TurnStep(Dir=dir_l, steps=6400, stepdelay=self.v_l)
		self.motor_r.TurnStep(Dir=dir_r, steps=6400, stepdelay=self.v_r)	

		# todo: if 'esc':
		if key == 'esc':
			self.motor_l.stop()
			self.motor_r.stop()

from .teleop import Teleop
if __name__ == '__main__':
	try:
		v = 0.1
		u = 0.1
    
		key_list = ['a', 'd', 's', 'w']
		topic_name = 'key_press'
    
		controller = WASDController(key_list,topic_name)
        
		rospy.init_node('motor_node', anonymous=True)
		rospy.Subscriber(String, controller.callback)
    
		rospy.spin()
  except rospy.ROSInterruptException:
    pass
