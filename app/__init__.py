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
#Using Sendgrid  to send emails in heroku app instead of smtp.gmail
from sendgrid  import *
from sendgrid.helpers.mail import *

from werkzeug.security import generate_password_hash
sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))


#RASA NLU
#from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
#from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter
#from rasa_nlu.components import ComponentBuilder
#builder = ComponentBuilder(use_cache=True)
#config = RasaNLUConfig("sample_configs/config_spacy.json")
#training_data = load_data ('data/examples/rasa/demo-rasa.json')
#trainer = Trainer(RasaNLUConfig("sample_configs/config_spacy.json"))
#trainer.train(training_data)
#model_directory = trainer.persist('./projects/default/') #returns the directory the model is stored in
#print(model_directory)

from .train import *

#config= RasaNLUConfig("/var/www/new/registration/sample_configs/config_spacy.json")
#interpreter = Interpreter.load(model_directory,config,builder)
#print('rasa')
#print (interpreter_clone)
#print (interpreter.parse(u"Hi my name is Paolo"))


def generate_random_password():
	''' from https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python'''
	return ''.join(choice(string.ascii_uppercase) for i in range(randint(6,12)))
@app.route('/queryrasabot',methods = ['GET'])
def query():
	#from .train import *
	#try:
        #    from .train import interpreter
	#except :
	#	print ('train.py error')
	dict = interpreter.parse(u"my name is carlos")
	return dict
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
			print(appbuilder.get_url_for_index)
			return redirect(appbuilder.get_url_for_index)
		else:
			appbuilder.sm.del_register_user(reg)
			return render_template(activation_template,
							   username=reg.username,
							   first_name=reg.first_name,
							   last_name=reg.last_name,
							   appbuilder=appbuilder)
def send_subscription_email(registeruser,random_generated_password):
	email_template='custom_register.html' # default register mail from flask_appbuilder
	#Using sendgrid instead of Flask_Mail for heroku
	#base_url='http://localhost:8080' #change localhost if deployed
	#base_url = 'https://ifabsampleapp.herokuapp.com'
	#base_url='https://intuitionmachine.ml'
	base_url='https://chat-intuitionfabric.herokuapp.com'
	print(base_url)
	#url=base_url+'/register/activation/'+registeruser.registration_hash
	url=base_url+"/login"
	#content=Content("text/plain","hello world")
	#msg = render_template('appbuilder/custom_register.html',username=registeruser.email,
	#							   first_name=registeruser.first_name,
	#							   password=random_generated_password,
	#							   hash=registeruser.registration_hash,url=url,last_name=registeruser.last_name)
	msg = render_template('appbuilder/custom_register.html',username=registeruser.email,
								first_name=registeruser.first_name,
								password=random_generated_password,
								url=url,
								last_name=registeruser.last_name)
	#fromEmail=os.environ.get('MAIL_USERNAME')
	from_email = Email("eduardofranivaldez@gmail.com")
	subject = "Intuition Fabric Account Activation"
	toEmail=   registeruser.email
	to_email = Email(toEmail)
	content = Content("text/html",msg)
	mail = Mail(from_email, subject, to_email, content)
	try:
		response=sg.client.mail.send.post(request_body=mail.get())
		print(response.status_code)
		print(response.body)
		print(response.headers)
	except Exception as e:
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

@app.route("/fbmessenger",methods=['GET'])
def handle_verification():
	'''Verifies facebook webhook subscription
		Successful when verify_token is same as token sent by facebook app
	'''
	if (request.args.get('hub.verify_token', '') == VERIFY_TOKEN):
		print("succefully verified")
		return request.args.get('hub.challenge', '')
	else:
		print("Wrong verification token!")
		return "Wrong validation token"
@app.route("/fbmessenger",methods=['POST'])
def handle_message():
	'''Handle messages sent by facebook messenger to the applicaiton'''
	data = request.get_json()
	if data["object"] == "page":
		for entry in data["entry"]:
			for messaging_event in entry["messaging"]:
				if messaging_event.get("message"):
					sender_id = messaging_event["sender"]["id"]
					recipient_id = messaging_event["recipient"]["id"]
					message_text = messaging_event["message"]["text"]
					send_message_response(sender_id, chatbot_response(message_text))

	return "ok"
def send_message(sender_id, message_text):
	'''Sending response back to the user using facebook graph API'''
	r = requests.post("https://graph.facebook.com/v2.6/me/messages",
		params={"access_token": PAT},
		headers={"Content-Type": "application/json"},
		data=json.dumps({
		"recipient": {"id": sender_id},
		"message": {"text": message_text}
	}))
def chatbot_response(userQuery):
	request = ai.text_request()
	request.lang = 'de'  # optional, default value equal 'en'
	request.query = userQuery
	response = json.loads(request.getresponse().read().decode('utf-8'))
	print('r')
	print(response)
	responseStatus = response['status']['code']
	if (responseStatus == 200):
		if 'Great!' in response['result']['fulfillment']['speech']:
			contexts=response['result']['contexts']
			print("type")
			print (type(contexts))
			email=''
			firstname=''
			for context in contexts:
				if(context['name']=='ask-email'):
					print (context)
					email=context['parameters']['email']
					#firstname=context['parameters']['given-name.original']
			password=generate_random_password()
			print ('password')
			print(password)
			print ('email')
			print(email)
			print ('name')
			print (firstname)
			if db.session.query(MyUser).filter_by(username=email).first() or db.session.query(MyUser).filter_by(email=email).first() :
				return ("Sorry mate. There is already an account associated with %s. Try using another email."%email)
			if len(email)>1 and len(firstname)<1:
				print("given name failed.")
				#registeruser = appbuilder.sm.add_register_user(email,firstname,firstname,email,password)
				firstname=email
			if len(email)>1 and len(firstname)>1:
				print (appbuilder.sm.find_role(appbuilder.sm.auth_user_registration_role))
				registeruser= appbuilder.sm.add_user(username=email,first_name=firstname,last_name=firstname,email=email,role=appbuilder.sm.find_role(appbuilder.sm.auth_user_registration_role),password=password )
				if registeruser:
					send_subscription_email(registeruser,password)
					#Should we try to catch email ?
					return("Thanks for subscribing! Your username is %s and initial password is %s. Feel free to change it under Profile Settings, once you have logged in."%(email,password))
				else:
					return ("Sorry, we cannot register you at the moment. Please try again later.")
		return (response['result']['fulfillment']['speech'])
	else:   #problem with service
		return ("Sorry, I couldn't understand that question")

def send_message_response(sender_id,message_text):
	sentenceDelimeter="."
	messages = message_text.split(sentenceDelimeter)
	for message in messages:
		send_message(sender_id,message)

@app.route("/querychatbot/<query>" ,methods=['POST','GET','OPTIONS'])
@cross_origin()
def get_chatbot_response(query):
	request = ai.text_request()
	request.lang = 'de'  # optional, default value equal 'en'
	request.query = query
	response = json.loads(request.getresponse().read().decode('utf-8'))
	responseStatus = response['status']['code']
	if (responseStatus == 200):
		print(type(response['result']['fulfillment']['speech']))
		if 'Great!' in response['result']['fulfillment']['speech']:
			contexts=response['result']['contexts']
			print("type")
			print (type(contexts))
			email=''
			firstname=''
			for context in contexts:
				if(context['name']=='ask-email'):
					print (context)
					email=context['parameters']['email']
					#firstname=context['parameters']['given-name.original']
			password=generate_random_password()
			print ('password')
			print(password)
			print ('email')
			print(email)
			print ('name')
			print (firstname)
			if db.session.query(MyUser).filter_by(username=email).first() or db.session.query(MyUser).filter_by(email=email).first() :
				return ("Sorry mate. There is already an account associated with %s. Try using another email."%email)
			if len(email)>1 and len(firstname)<1:
				print("given name failed.")
				#registeruser = appbuilder.sm.add_register_user(email,firstname,firstname,email,password)
				firstname=email
			if len(email)>1 and len(firstname)>1:
				print (appbuilder.sm.find_role(appbuilder.sm.auth_user_registration_role))
				registeruser= appbuilder.sm.add_user(username=email,first_name=firstname,last_name=firstname,email=email,role=appbuilder.sm.find_role(appbuilder.sm.auth_user_registration_role),password=password)
				if registeruser:
					send_subscription_email(registeruser,password)
					#Should we try to catch email ?
					return("Thanks for subscribing! Your username is %s and initial password is %s. Feel free to change it under Profile Settings, once you have logged in."%(email,password))
				else:
					return ("Sorry, we cannot register you at the moment. Please try again later.")
		return (response['result']['fulfillment']['speech'])
	else:	#problem with service
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
