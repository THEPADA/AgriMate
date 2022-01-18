import threading
from DRV8825 import DRV8825


class Motor():
    def __init__(self, dir_pin, step_pin, enable_pin, mode_pins, min_w=0.0001):
        self.driver = DRV8825(dir_pin, step_pin, enable_pin, mode_pins)
        self.driver.SetMicroStep('hardward' ,'fullstep')
        self.min_w = min_w
        
        self.w = 0  # in degrees per second
        self.terminate = False        
        threading.Thread(target=self.motor_thread).start()

    def motor_thread(self):
        while self.terminate:
            if abs(self.w) > self.minimum_w:
                stepdelay = 360/(6400*self.w)

                self.driver.digital_write(self.step_pin, True)
                time.sleep(stepdelay)
                self.driver.digital_write(self.step_pin, False)
                time.sleep(stepdelay)
            else:
                self.driver.stop()
        self.driver.stop()

    def update_w(self, w):
        self.w = w
    
    def terminate(self):
        self.terminate = True
