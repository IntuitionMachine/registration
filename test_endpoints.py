from app import app
import unittest

#from app.models import User
from app.models import MyRegisterUser
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
		result = self.app.get('/register/form',content_type='html/text',follow_redirects=True)
		self.assertTrue(b'Fill out the registration form' in result.data)

	def test_login(self):
		"Assert that the user lands on login page successfully"
		result = self.app.get('/login',follow_redirects=True)
		print(result)
		self.assertIn(b'Enter your login and password below',result.data)
		#self.assertEqual(result.status_code,301)

	#def test_correct_login(self):
	#	"ensure login behaves correctly given the correct credentials"
	#	result = self.app.post('/login'
	#		,data=dict(username='admin',password='admin')
	#		,follow_redirects=True 
	#		)
	#	self.assertEqual(result.status_code,200)

	def test_incorrect_login(self):
		"ensure login behaves correctly given the incorrect credentials"
		result = self.app.post('/login'
			,data=dict(username='nonexisting',password='nonexisting') 
			)
		self.assertIn(b'You should be redirected',result.data)			#will be redirected to login page
	#def test_incorrect_login_context(self):
	#	"ensure login prompts error message  given the incorrect credentials"
	#	result = self.app.post('/login'
	#		,data=dict(username='nonexisting',password='nonexisting')
	#		,follow_redirects=True
	#		,content_type='html/text' 
	#		)
	#	self.assertIn(b'Invalid login', result.data)
	#def test_correct_admin_login_context(self):
	#	"ensure contents after login is correct after correct admin credentials input"
	#	self.app.post('/login'
	#		,data=dict(username='admin',password='admin')
	#		,follow_redirects=True)
	#	result=self.app.get('/',follow_redirects=True,content_type='html/text' )
	#	print("AAAAA")
	#	print (result)
	#	self.assertTrue(b'Security' in result.data)

	#def test_logout(self):
	#	"ensures that logout behaves correctly"
	#	#must be logged in before you can log out
	#	self.app.post('/login'
	#		,data=dict(username='admin',password='admin')
	#		,follow_redirects=True)
	#	result=self.app.get('/logout' ,follow_redirects=True,content_type='html/text')
	#	self.assertFalse(b'Security' in result.data)
	def test_unique_email(self):
		user1=MyRegisterUser(first_name='john',last_name='john',username='john3',password='password',email='john3@email.com')
		db.session.add(user1)
		db.session.commit()
		email=user1.email
		
	#helper methods
	def register(self,email,password1,conf_password1,firstname,lastname,username):
		x= self.app.post('/register/form',data=dict(email=email,password=password1,conf_password=conf_password1,first_name=firstname,last_name=lastname,username=username),follow_redirects=False)
		#print(x)
		return x
	def login(self,username,password):
		return self.app.post('/login',data=dict(username=username,password=password),follow_redirects=True)
	def logout(self):
		return self.app.post('/logout',follow_redirects=True)
	def test_valid_user_registration(self):
		print ('valid reg')
		response=self.register('john12345@yahoo.com','password123','password123','firstname','lastname','john12345')
		print(response)
		#self.assertEqual(response.status_code,302)
		self.assertIn(b'Registration sent to your email',response.data)
	def test_invalid_user_registration_password_must_match(self):
		print('invalid reg')
		response=self.register('alice@gmail.com','password','anotherpassword','firstname','lastname','alice')
		print(response)
		self.assertIn(b'Passwords must match',response.data)
			
if __name__ == "__main__":
	unittest.main()
