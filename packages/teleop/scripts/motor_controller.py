import rospy
from std_msgs.msg import String
# from DRV8825 import DRV8825


class WASDController:
    # todo: need the teleop class to publish eg. w_p, w_p, w_p, w_p, w_r
    def __init__(self, topic_name='key_press', w_straight=1.0, w_turn=0.5, rate=10):
        
        self.topic_name = topic_name
        self.sub = rospy.Subscriber(topic_name, String, callback=self.callback)

        self.w_straight = w_straight
        self.w_turn = w_turn

        self.rate = rospy.Rate(rate)
        
        # self.motor_l = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        # self.motor_l.SetMicroStep('hardward' ,'fullstep')
		
        # self.motor_r = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
        # self.motor_r.SetMicroStep('hardward' ,'fullstep')

        self.w_l = 0
        self.w_r = 0

        self.pressed_key = []

    def format_data(self, data):
        data = data.data
        data = data.replace(']', '')
        data = data.replace('[', '')
        data = data.replace("'", "")
        data = data.replace(' ', "")
        data = data.split(',')
        return data

    def callback(self, data):
        data = self.format_data(data)

        self.w_l = 0
        self.w_r = 0
            
        if 'w' in data:
            self.w_l += self.w_straight
            self.w_r += self.w_straight

        if 's' in data:
            self.w_l -= self.w_straight
            self.w_r -= self.w_straight

        if 'a' in data:
            self.w_l -= self.w_turn
            self.w_r += self.w_turn

        if 'd' in data:
            self.w_l += self.w_turn
            self.w_r -= self.w_turn

    def run(self):
        while not rospy.is_shutdown():

            if self.w_l < 0:
                dir_l = 'backward'
            else:
                dir_l = 'forward'
        
            if self.w_r < 0:
                dir_r = 'backward'
            else:
                dir_r = 'forward'

            # todo: deal with divide by zero
            # step_delay_l = 360/(self.w_l*6400)
            # step_delay_r = 360/(self.w_r*6400)

            # self.motor_l.TurnStep(Dir=self.dir_l, steps=6400, stepdelay=step_delay_l)
            # self.motor_r.TurnStep(Dir=self.dir_r, steps=6400, stepdelay=step_delay_r)

            rospy.loginfo(str([self.w_l, self.w_r]))

            # If callback not ran within rate.sleep, will set these to zero
            self.w_l = 0
            self.w_r = 0
            self.rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('motor_controller_node', anonymous=True)
        c = WASDController()
        c.run()
    except rospy.ROSInterruptException:
        pass
