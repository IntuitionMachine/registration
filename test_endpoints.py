from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
	
	def setUp(self):
		"""Set up test application client"""
		self.app = app.test_client() 
		self.app.testing = True
	#def tearDown(self):
	#	"""Clear DB after running tests"""
	#	db.todos.remove({})

	def test_index(self):
		"Assert that the user lands on index page successfully"
		result = self.app.get('/')
		self.assertEqual(result.status_code,200)

	def test_index_context(self):
		"Assert that the index page returns correct content"
		result = self.app.get('/',content_type='html/text')
		self.assertIn(b'Subscribe To Intuition Machine',result.data)
		print(self.assertIn(b'Subscribe To Intuition Machine',result.data))
	def test_register_context(self):
		"Assert that the registration page returns correct content"
		result = self.app.get('/register/form',content_type='html/text')

		self.assertTrue(b'Fill out the registration form' in result.data)

	def test_login(self):
		"Assert that the user lands on login page successfully"
		result = self.app.get('/login')
		self.assertEqual(result.status_code,301)

	def test_correct_login(self):
		"ensure login behaves correctly given the correct credentials"
		result = self.app.post('/login'
			,data=dict(username='admin',password='admin')
			,follow_redirects=True 
			)
		self.assertEqual(result.status_code,200)

	def test_incorrect_login(self):
		"ensure login behaves correctly given the incorrect credentials"
		result = self.app.post('/login'
			,data=dict(username='nonexisting',password='nonexisting')
			,follow_redirects=True 
			)
	
		self.assertEqual(result.status_code,200)
	def test_incorrect_login_context(self):
		"ensure login prompts error message  given the incorrect credentials"
		result = self.app.post('/login'
			,data=dict(username='nonexisting',password='nonexisting')
			,follow_redirects=True
			,content_type='html/text' 
			)
		self.assertIn(b'Invalid login', result.data)
	def test_correct_admin_login_context(self):
		"ensure contents after login is correct after correct admin credentials input"
		self.app.post('/login'
			,data=dict(username='admin',password='admin')
			,follow_redirects=True)
		result=self.app.get('/',follow_redirects=True,content_type='html/text' )
		print("AAAAA")
		print (result)
		self.assertTrue(b'Security' in result.data)

	def test_logout(self):
		"ensures that logout behaves correctly"
		#must be logged in before you can log out
		self.app.post('/login'
			,data=dict(username='admin',password='admin')
			,follow_redirects=True)
		result=self.app.get('/logout' ,follow_redirects=True,content_type='html/text')
		self.assertFalse(b'Security' in result.data)
if __name__ == "__main__":
	unittest.main()