from DRV8825 import DRV8825
import threading

class Motor():
    def __init__(self, dir_pin, step_pin, enable_pin, mode_pins):
        self.driver = DRV8825(dir_pin, step_pin, enable_pin, mode_pins)
        self.driver.SetMicroStep('hardward' ,'fullstep')

        self.minimum_w = 0.0001

        self.keep_turning = False
        threading.Thread(target=self.turn_thread).start()

    def turn_thread(self):
        while True:
            if self.keep_turning:
                if abs(self.w) > self.minimum_w:
                    stepdelay = 360/(6400*self.w)
                        
                    self.driver.digital_write(self.step_pin, True)
                    time.sleep(stepdelay)
                    self.driver.digital_write(self.step_pin, False)
                    time.sleep(stepdelay)
            else:
                self.driver.stop()

    def update_w(self, w):
        self.w = w

    def turn(self, keep_turning):
        self.keep_turning = keep_turning
