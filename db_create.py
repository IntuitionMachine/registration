from app import db
from app.models import MyUser,MyRegisterUser

db.create_all()
db.session.commit() 