#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/ifab/")
import os 

from ifab import app as application
print(os.environ.get('SECRET_KEY')
application.secret_key = os.environ.get('SECRET_KEY')

