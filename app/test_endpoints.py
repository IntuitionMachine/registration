from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
	def test_index(self):
		"Assert that the user lands on login page successfully"
		result = self.app.get('/',content_type='html/text')
		self.assertEqual(result.status_code,200)


if __name__ == "__main__":
    unittest.main()