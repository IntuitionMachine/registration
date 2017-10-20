from app import db
from app.models import MyUser

db.create_all()
db.session.commit() 
