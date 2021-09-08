from Motors.Motors import *
import sys
import os
sys.path.append(os.getcwd())
from Utils.Logging.Logging import *

class Commander:
    def Balance(self, actuation):
        if actuation < 0:
                move_backward(abs(actuation))
                
        else:
                move_forward(abs(actuation))