from app import app
import os
from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)


#print(os.get('SQLALCHEMY_DATABASE_URI'))

if __name__ == '__main__':
     app.run(debug=True,threaded=True)

