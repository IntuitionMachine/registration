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
#import apiai
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
VERIFY_TOKEN=os.environ.get('VERIFYF_TOKEN')
PAT =os.environ.get('PAT')

#API AI Credentials
CLIENT_ACCESS_TOKEN=os.environ.get('CLIENT_ACCESS_TOKEN')
#ai=apiai.ApiAI(CLIENT_ACCESS_TOKEN)
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
#ai=apiai.ApiAI(CLIENT_ACCESS_TOKEN)
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

from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Metadata, Interpreter
from .train import interpreter

#RASA CORE
from rasa_core.actions import Action
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy

def generate_random_password():
	''' from https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python'''
	return ''.join(choice(string.ascii_uppercase) for i in range(randint(6,12)))


agent=Agent.load("models/dialogue",interpreter=interpreter)
print(agent.handle_message("hi"))
print(agent.handle_message("My name is Giannis Atentekoumpo"))


#RASA CORE

import random
ask_name = [ "Hello there! What is your name? ", "Hey there, what is your name?", "What is your name?", "Name please? "]

#global var
firstname=''
email=''

import re

def extract_email(text):
	#extracts the word with @ , gets all non space characters beforeand after@
	m=re.search("\S*@\S*",text)
	try:
		email=m.group()
		return email
	except: #if no word with @
		return False
def extract_name(text):
	if "i am " in text.lower():
		print("1")
		#temp=text.lower().split("i am")
		m=re.search("i am\s*([^.]+|\S+)",text.lower())
		print(m.group())
		print(m.group(1))
	elif "call me" in text.lower():
		print("2")
		#temp.text.lower().split("call me")
		m=re.search("call me\s*([^.]+|\S+)",text.lower())
		print(m.group())
		print(m.group(1))
	elif "i'm" in text.lower():
		print("3")
		#text=temp.lower().split("i'm")
		m=re.search("i'm\s*([^.]+|\S+)",text.lower())
		print(m.group())
		print(m.group(1))
	elif "name is" in text.lower():
		print("4")
		#text=temp.lower().split("name is")
		m=re.search("name is\s*([^.]+|\S+)",text.lower())
		print(m.group())
		print(m.group(1))
	elif "is my name" in text.lower():
		print("5")
		m = re.search("\w+(?=\s*is my name[^/])",text.lower())
		print(m.group())
		print(m.group(1))
	else:
		print("0")
		return False
		#text=temp.lower.split(" ")
		#text=text[-1]
		#print("name was: ")
		#print(text)
	name=m.group(1)
	#name=text[-1].lstrip().rstrip() #removes white space characters before and after the name
	print(name)
	return name

@app.route('/queryrasabot/<query>',methods = ['GET'])
def rasanluquery(query):
	response = agent.handle_message(query)
	#response = interpreter.parse(query)
	#firstname=''
	#email=''
	global firstname
	global email
	print(response)
	#return jsonify(response)
	if response['intent']['name']=='greet':
		return  random.choice(ask_name)
	elif (response['intent']['name']=='get_name'):
		try:
			if response['entities'][0]:
				print("NAME ENTITIES")
				print(response['entities'][0]['entity'])
				if response['entities'][0]['entity']=='first_name':
					firstname=response['entities'][0]['value']
					#print("fname")
					#print(firstname)
					#return "hello there %s ! what is your email address?"%firstname
		except:
			print("e1")
			print(response['text'])
			firstname=extract_name(response['text'])
			if firstname!=False:
				pass
			else:
				return "Sorry. What is your first name again?"
		print("fname")
		print(firstname)
		return "hello there %s ! what is your email address?"%firstname

	elif response['intent']['name']=='get_email':
		try:
			if response['entities'][0]:
				print ("EMAIL ENTITY")
				print(response['entities'][0]['entity'])
				if response['entities'][0]['entity']=='email':
					email = response['entities'][0]['value']
					password = generate_random_password()
					if len(firstname)<1:
						firstname=email
					if db.session.query(MyUser).filter_by(username=email).first() or db.session.query(MyUser).filter_by(email=email).first() :
						return ("Sorry mate. There is already an account associated with %s. Try using another email. If you have further inquiries, you may send them to info@intuitionmachine.com."%email)
					print (appbuilder.sm.find_role(appbuilder.sm.auth_user_registration_role))
					#registeruser= appbuilder.sm.add_user(username=email,first_name=firstname,last_name="",email=email,role=appbuilder.sm.find_role(appbuilder.sm.auth_user_registration_role),password=password )
					#if registeruser:
					#	send_subscription_email(registeruser,password)
					#	#Should we try to catch email ?
					#	return("Thanks for subscribing %s! Your username is %s and initial password is %s. Feel free to change it under Profile Settings, once you have logged in. We will email you this registration details as well."%(firstname,email,password))
					#else:
					#	return ("Sorry, we cannot register you at the moment. Please try again later.")
		except:
			print("e2")
			print(response['text'])
			email=extract_email(response['text'])
			if email!=False:
				pass
			else:
				return("Sorry I did not understand that. Can you repeat your email address?")
		registeruser= appbuilder.sm.add_user(username=email,first_name=firstname,last_name="",email=email,role=appbuilder.sm.find_role(appbuilder.sm.auth_user_registration_role),password=password )

		if registeruser:
			send_subscription_email(registeruser,password)
			#Should we try to catch email ?
			return("Thanks for subscribing %s! Your username is %s and initial password is %s. Feel free to change it under Profile Settings once you haved logged in"%(firstname,email,password))
		else:
			return ("Sorry, we cannot register you at the moment. Please try again later.")

	return "Sorry I did not get that. Can you repeat that again?"
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
					return("Thanks for subscribing %s! Your username is %s and initial password is %s. Feel free to change it under Profile Settings, once you have logged in."%(firstname,email,password))
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
