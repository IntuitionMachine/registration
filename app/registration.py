from flask_appbuilder.security.registerviews import BaseRegisterUser
from flask_appbuilder.security.sqla.manager import SecurityManager
from flask_appbuilder import expose
from flask import request
import requests
class MyRegisterUserDBView(BaseRegisterUser):
	register_template = 'appbuilder/register.html'
	error_message= 'Not possible to register at the moment. Please try again later.'
	message = 'Registration sent to your email!'
	redirect_url = '/'


	def form_get(self,form):
		pass
	def form_post(self,form):
		geoIP = request.remote_addr
		url = 'http://freegeoip.net/json/'+geoIP
		req = request.get(url)
		reqJSON = req.json()
		geoLoc = reqJSON['country_name']
#class MySecurityManager(SecurityManager):
#               registeruserdbview = MyRegisterUserDBView		
