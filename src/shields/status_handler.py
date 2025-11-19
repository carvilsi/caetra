import sys
import os
import tempfile

# caetra imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import constants 
from caetra_exceptions import MaxActionReached

class StatusHandler(object):
    
    counter = 0
    time_lapse_ns = 0
    
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

    def can_be_sent(self, current_ns, max_actions, cool_down_time):
        self.inccount()
        if self.counter == max_actions:
            self.time_lapse_ns = current_ns
        elif self.counter > max_actions:
            if ((current_ns - self.time_lapse_ns) / constants.NS_TO_S) <= cool_down_time:
                raise MaxActionReached("Reached max actions; not sending")
            else:
                self.counter = 0



 
