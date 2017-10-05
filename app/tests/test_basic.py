import os
import unittest

from app import app,db

TEST_DB = 'test.db'

class BasicTests(unittest.TestCase):
	"Set up and tear down"

	#execute prior to each test
	def setUp(self):
		app.config['TESTING']=True
		app.config['WTF_CRSF_ENABLED']=False
if __name__ == "__main__":
    unittest.main()