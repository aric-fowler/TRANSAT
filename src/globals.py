'''
Global variables shared between all TRANSAT Tools

Author:     Aric Fowler
Python:     3.10.12
Updated:    Feb 2024
'''
import os
import datetime

logFormat = '%(asctime)s %(levelname)s: %(message)s\n'
logDateFormat = '%b-%d-%Y_%I-%M%p'

here = os.getcwd()
now = datetime.datetime.now().strftime(logDateFormat)

workDir = 'work/'
logDir = 'log/'
debugDir = 'debug/'