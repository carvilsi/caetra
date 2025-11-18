import sys
import os
import tempfile

# caetra imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import constants 

class StatusHandler(object):
    
    counter = 0
    time_lapse_ns
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(StatusHandler, cls).__new__(cls)
        return cls.instance

    def get_counter(self):
        return self.counter

    def inccount(self):
        self.counter += 1

    def set_time_lapse(self, value):
        self.time_lapse_ns = value

    def is_able_to_send(self, current_ns):
        if ((time_lapse_ns - current_ns) / constants.NS_TO_S) >= constants.COOL_DOWN_TIME_TO_SEND:
            return True
        else:
            return False


 
