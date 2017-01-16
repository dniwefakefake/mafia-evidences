import sys,os
file_location = os.path.dirname(os.path.realpath(__file__))
sys.path.append(file_location)
os.chdir(file_location)
from evidences import app as application
