from app import db
from models import MyUser,MyRegisterUser

db.create_all()
db.session.commit() 