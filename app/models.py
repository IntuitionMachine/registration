from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey ,Boolean,Date
from sqlalchemy.orm import relationship
"""
You can use the extra Flask-AppBuilder fields and Mixin's
AuditMixin will add automatic timestamp of created and modified by wh
"""

#extend default User class of  F.A.B
from flask_appbuilder.security.sqla.models import User,RegisterUser
#from .app import db
class CountryStat(Model):
	__tablename__ = 'countrystat'
	id=Column(Integer,primary_key=True)
	country=Column(String(70))
	count=Column(Integer())

class Profile(Model):
	__tablename__ = 'profiles'
	id = Column(Integer,primary_key=True)
	fname = Column(String(50))
	lname = Column(String(50))
	birthday=Column(String(50))
	email=Column(String(255),unique=True)
	streetAddress=Column(String(255))
	country=Column(String(255))
	city=Column(String(255))
	state=Column(String(255))
	zipCode=Column(String(255))
	ethAddress=Column(String(255))
	govID=Column(String(255))
	geoIP=Column(String(255))
	geoLoc=Column(String(255))
	password=Column(String(255))
	#role_id = Column(Integer(), db.ForeignKey('roles.id'))
	is_admin = Column(Boolean(), default=False)

class MyUser(User):
		#Extend User of F.A.B
		birthday=Column(Date())
		user_email=Column(String(255),unique=True)
		streetAddress=Column(String(255))
		country=Column(String(255))
		city=Column(String(255))
		state=Column(String(255))
		zipCode=Column(String(255))
		ethAddress=Column(String(255))
		govID=Column(String(255))
		geoIP=Column(String(255))				
		geoLoc=Column(String(255))

class MyRegisterUser(RegisterUser): 
#Extend Register User of F.A.B
	birthday=Column(String(50))
	user_email=Column(String(255),unique=True)
	streetAddress=Column(String(255))
	country=Column(String(255))
	city=Column(String(255))
	state=Column(String(255))
	zipCode=Column(String(255))
	ethAddress=Column(String(255))
	govID=Column(String(255))
	geoIP=Column(String(255))
	geoLoc=Column(String(255))