import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../senders'))

import config_parser

config = config_parser.read()

# one function to rule them all
def call_em_all():
    print(config)
    



