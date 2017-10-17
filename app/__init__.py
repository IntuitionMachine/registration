import logging
from flask import Flask,render_template,request,redirect,jsonify, url_for
from flask_appbuilder import SQLA, AppBuilder
from sqlalchemy import func

from .models import MyUser,CountryStat
#Override IndexView
from app.index import MyIndexView
#Override Security Manager
from .sec import MySecurityManager

#chatterbot
#from chatterbot import ChatBot 
#from chatterbot.trainers import ChatterBotCorpusTrainer
import requests
import apiai
import json
"""
 Logging configuration
"""
# english_bot=ChatBot("Gordon Ramsey",storage_adapter='chatterbot.storage.SQLStorageAdapter',database_uri='postgresql://postgres:admin@localhost/intuitionmachine')
# english_bot.set_trainer(ChatterBotCorpusTrainer)
# english_bot.train("chatterbot.corpus.english")
"""  Sample API.AI chatbot in API.AI and Facebook
is hosted in http://botsandcrypto.herokuapp.com/
sample Facebook Page is https://www.facebook.com/Bots-and-Cryptocurrency-165108627403522/

"""
from .forms import MyRegisterUserDBForm
from flask_babel import lazy_gettext
import os
from flask_cors import CORS,cross_origin
#from flask_sslify import SSLify  #to make all incoming request of Flask HTTPS


#Credentials For OpenWeatherAPI
OWMKEY=os.environ.get('OWMKEY')
#FB Credentials
VERIFY_TOKEN=os.environ.get('VERIFY_TOKEN')
PAT =os.environ.get('PAT')

#API AI Credentials
CLIENT_ACCESS_TOKEN=os.environ.get('CLIENT_ACCESS_TOKEN')

ai=apiai.ApiAI(CLIENT_ACCESS_TOKEN)

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS']='application/json'
print(CLIENT_ACCESS_TOKEN)
app.config.from_object('config')
db = SQLA(app)
#sslify = SSLify(app)
appbuilder = AppBuilder(app, db.session,indexview=MyIndexView,security_manager_class=MySecurityManager)
ai=apiai.ApiAI(CLIENT_ACCESS_TOKEN)
#Using Sendgrid for heroku app insteadof Flask_Mail
#from flask_mail import Mail,Message
from flask_appbuilder.baseviews import expose
from flask_appbuilder.security.registerviews import RegisterUserDBView
from random import randint,choice
import string
from flask_appbuilder.security.sqla.models import User,RegisterUser
import sendgrid
from sendgrid.helpers.mail import *
SENDGRID_API_KEY=os.environ.get('SENDGRID_API_KEY')
sg=sendgrid.SendGridAPIClient(SENDGRID_API_KEY)


@app.route('/')
def hello_world():
    return 'hello world!'
def generate_random_password():
	''' from https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python'''
	#N=random.randint(6, 12)
	#return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
	return ''.join(choice(string.ascii_uppercase) for i in range(randint(6,12)))
@expose('/activation/<string:activation_hash>')
def activation(activation_hash):
		"""
			Endpoint to expose an activation url, this url
			is sent to the user by email, when accessed the user is inserted
			and activated
		"""
		activation_template='appbuilder/myactivation.html'
		error_message=lazy_gettext('Not possible to register you at the moment, try again later')
		false_error_message = lazy_gettext('Registration not found')
		reg = appbuilder.sm.find_register_user(activation_hash)
		if not reg:
			#print('0')
			log.error(c.LOGMSG_ERR_SEC_NO_REGISTER_HASH.format(activation_hash))
			flash(as_unicode(false_error_message), 'danger')
			print(appbuilder.get_url_for_index)
			return redirect(appbuilder.get_url_for_index)
		if not appbuilder.sm.add_user(username=reg.username,
											   email=reg.email,
											   first_name=reg.first_name,
											   last_name=reg.last_name,
											   role=appbuilder.sm.find_role(
													   appbuilder.sm.auth_user_registration_role),
											   hashed_password=reg.password):
			flash(as_unicode(error_message), 'danger')
			#print('1')
			print(appbuilder.get_url_for_index)
			return redirect(appbuilder.get_url_for_index)
		else:
			print('2')
			appbuilder.sm.del_register_user(reg)
			#print ('here')
			return render_template(activation_template,
							   username=reg.username,
							   first_name=reg.first_name,
							   last_name=reg.last_name,
							   appbuilder=appbuilder)
def send_subscription_email(registeruser,random_generated_password):
	print ('hash')
	print (registeruser.registration_hash)
	email_template='custom_register.html' # default register mail from flask_appbuilder
	print(email_template)
	#Using sendgrid instead of Flask_Mail for heroku
	from_email=os.environ.get('MAIL_USERNAME')
	subject = 'From sendgrid'
	to_email= registeruser.email
	
	#mail = Mail(app)
	#msg = Message()
	#msg.subject = lazy_gettext('Account activation')
        #base_url='http://localhost:8080' #change localhost if deployed
	#base_url = 'https://ifabsampleapp.herokuapp.com'
	#base_url ='http://128.199.246.202'
	#base_url='https://intuitionmachine.ml'
	base_url='https://chat-intuitionfabric.herokuapp.com'
	print(base_url)
	url=base_url+'/register/activation/'+registeruser.registration_hash
	print ('url')
	print(url)
	msg.html = render_template('appbuilder/custom_register.html',username=registeruser.email,
								   first_name=registeruser.first_name,
								   password=random_generated_password,
								   hash=registeruser.registration_hash,url=url,last_name=registeruser.last_name)
	context=Context("text/html",msg.html)
	mail=Mail(from_email,subject,to_email,context)
	#msg.recipients = [registeruser.email]
	try:
		#Flask_Mail
		#mail.send(msg)

		#SendGrid
		response=sg.client.mail.send.post(request_body=mail.get())
		print(response.status_code)
		print(response.body)
		print(response.headers)
	except Exception as e:
		#log.error("Send email exception: {0}".format(str(e)))
		print ("Send email exception: {0}".format(str(e)))
		return False
	return True
@app.route("/update/<oldCountry>/<countryData>/<id>/<ipaddr>")
def update_user(id,oldCountry,countryData,ipaddr):
	""" Update CountryStats Tables and IP Address Of User"""
	print(id)
	print(oldCountry)
	print(countryData)
	print(ipaddr)
	tempUser=db.session.query(MyUser).filter_by(id=id).first()
	tempCountry=db.session.query(CountryStat).filter_by(country=countryData).first()
	print(tempCountry)
	#if same IP addr, don't save
	if tempUser.geoIP==ipaddr:
		pass
	else:
		tempUser.geoIP=ipaddr
		url = 'http://freegeoip.net/json/'+ipaddr
		req=requests.get(url)
		reqJSON = req.json()
		geoLoc = reqJSON['country_name']
		tempUser.geoLoc=geoLoc
	# if same country as before, do nothing
	if oldCountry==countryData:
		print("same ",tempUser.country,countryData)
		return str(id) #exit
	else:   
		if oldCountry=='None': #Don't add to DB or subtract
			pass
		else:
			updateCountry=db.session.query(CountryStat).filter_by(country=oldCountry).first()
			if updateCountry:
				updateCountry.count-=1
				print("old")
	if tempCountry: #if country already exists      
		tempCountry.count+=1
		print("+1")
	else:
		print("new")
		newCountry=CountryStat(country=countryData,count=1)
		db.session.add(newCountry)  
	db.session.commit()
	return str(id)
@app.route("/get/countries")
def get_country_count():
		countryStat=db.session.query(MyUser.country,func.count(MyUser.country)).group_by(MyUser.country).all()
		countries=[]
		count=[]
		for i in countryStat:
			countries.append(i[0])
			count.append(i[1])
		print(countryStat)
		return jsonify({'countries':countries ,'count':count})

@app.route("/querychatbot/<query>" ,methods=['POST','GET','OPTIONS'])
@cross_origin()
def get_chatbot_response(query):
	request = ai.text_request()
	request.lang = 'de'  # optional, default value equal 'en'
	#request.session_id = "" #add unique session ID for each user
	request.query = query
	response = json.loads(request.getresponse().read().decode('utf-8'))
	responseStatus = response['status']['code']
	if (responseStatus == 200):
		print(type(response['result']['fulfillment']['speech']))
		if 'subscribing' in response['result']['fulfillment']['speech']:
			contexts=response['result']['contexts']
			print("type")
			print (type(contexts))
			
			for context in contexts:
				print (context)
				email=context['parameters']['email']
				firstname=context['parameters']['given-name']
			password=generate_random_password()
			print ('password')
			print(password)
			
			registeruser = appbuilder.sm.add_register_user(email,firstname,firstname,email,password)
			if registeruser:
				if send_subscription_email(registeruser,password):
					print("X")
				else:
					print ("Y")
					appbuilder.sm.del_register_user(registeruser)
					return 'Not possible to register(via chat) you at the moment, try again later'
			#else:
			#	return 'Cannot save to Database. Username or Email might have been already taken'
		return (response['result']['fulfillment']['speech'])
	else:
		return ("Sorry, I couldn't understand that question")
"""
from sqlalchemy.engine import Engine
from sqlalchemy import event
#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
	# Will force sqllite contraint foreign keys
	cursor = dbapi_connection.cursor()
	cursor.execute("PRAGMA foreign_keys=ON")
	cursor.close()
"""    
from app import models,views
db.create_all()
