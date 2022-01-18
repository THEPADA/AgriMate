import rospy
from std_msgs.msg import String
from .motor import Motor


class WASDController:
    def __init__(self, topic_name='key_press', w_straight=30.0, w_turn=15.0, rate=10):

        self.topic_name = topic_name
        self.sub = rospy.Subscriber(topic_name, String, callback=self.callback)

        # angular frequency in degrees / second
        self.w_straight = w_straight
        self.w_turn = w_turn

        self.rate = rospy.Rate(rate)    # rate needs to be slower or equal to key_press topic being published

        self.motor_l = Motor(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        self.motor_r = Motor(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))

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
            self.motor_l.update_w(self.w_l)
            self.motor_r.update_w(self.w_r)
            
            # todo: for debugging, can remove later
            rospy.loginfo(str([self.w_l, self.w_r]))
    
            # If callback not ran within rate.sleep, will set these to zero
            self.w_l = 0
            self.w_r = 0
            self.rate.sleep()
        
        self.motor_l.terminate()
        self.motor_r.terminate()
        

if __name__ == '__main__':
    try:
        rospy.init_node('motor_controller_node', anonymous=True)
        c = WASDController()
        c.run()
    except rospy.ROSInterruptException:
        pass
