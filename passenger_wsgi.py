# import imp
# import os
# import sys


# sys.path.insert(0, os.path.dirname(__file__))

# wsgi = imp.load_source('wsgi', 'hello.py')
# application = wsgi.hello
# 
import os
import sys

# Add your app's directory to the system path
sys.path.insert(0, '/home/johnjkeq/movie')

# Import your Flask app
from main import app as application  # 'app' matches the Flask app instance name in main.py

