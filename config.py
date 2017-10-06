import os
from flask_appbuilder.security.manager import AUTH_OID, AUTH_REMOTE_USER, AUTH_DB, AUTH_LDAP, AUTH_OAUTH
basedir = os.path.abspath(os.path.dirname(__file__))

# Your App secret key
SECRET_KEY = ''
# The SQLAlchemy connection string.
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

#HEROKU REMOTE DB
#SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')
#LOCAL DB
SQLALCHEMY_DATABASE_URI = ''
#SQLALCHEMY_DATABASE_URI = 'postgresql://root:password@localhost/myapp'

#Recaptcha Settings
#RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY =  ''
# Flask-WTF flag for CSRF
CSRF_ENABLED = True

#------------------------------
# GLOBALS FOR APP Builder 
#------------------------------
# Uncomment to setup Your App name
APP_NAME = "Intuition Fabric"

# Uncomment to setup Setup an App icon
APP_ICON = "static/img/intuitionmachine.png"

#----------------------------------------------------
# AUTHENTICATION CONFIG
#----------------------------------------------------
# The authentication type
# AUTH_OID : Is for OpenID
# AUTH_DB : Is for database (username/password()
# AUTH_LDAP : Is for LDAP
# AUTH_REMOTE_USER : Is for using REMOTE_USER from web server
#AUTH_TYPE = AUTH_DB
#AUTH_TYPE = AUTH_OAUTH
AUTH_TYPE=AUTH_DB
#GOOGLE_API_CLIENT_ID = '1073346562559-k45igodd0anqbnrbn40u1ie6q3oj4bmc.apps.googleusercontent.com'
#GOOGLE_API_CLIENT_SECRET = 'Rmuem4qinPp60nrP55R2ZCFO'
OAUTH_PROVIDERS = [
	 {'name':'twitter', 'icon':'fa-twitter',
		 'remote_app': {
			 'consumer_key':'',
			 'consumer_secret':'',
			 'base_url': 'https://api.twitter.com/1.1/',
			 'request_token_url': 'https://api.twitter.com/oauth/request_token',
			 'access_token_url': 'https://api.twitter.com/oauth/access_token',
			 'authorize_url': 'https://api.twitter.com/oauth/authenticate'}
	}
	,
	{'name': 'google', 'icon': 'fa-google', 'token_key': 'access_token',
		'remote_app': {
			'consumer_key':'',
			'consumer_secret':'',
			'base_url': 'https://www.googleapis.com/oauth2/v2/',
			'request_token_params': {
			  'scope': 'email profile'
			},
			'request_token_url': None,
			'access_token_url': 'https://accounts.google.com/o/oauth2/token',
			'authorize_url': 'https://accounts.google.com/o/oauth2/auth'}
	}
	]
	
	
	# }
# ]

# Uncomment to setup Full admin role name
#AUTH_ROLE_ADMIN = 'Admin'

# Uncomment to setup Public role name, no authentication needed
#AUTH_ROLE_PUBLIC = 'Public'

# Will allow user self registration
AUTH_USER_REGISTRATION = True

# The default user self registration role
AUTH_USER_REGISTRATION_ROLE = "Admin"

#Config For Flask-Mail necessary for User Registration
MAIL_PORT=587
MAIL_USE_SSL=False
MAIL_SERVER = 'smtp.gmail.com'
MAIL_USE_TLS = True
MAIL_USERNAME =  ''
MAIL_PASSWORD =  ''
MAIL_DEFAULT_SENDER =  ''

# When using LDAP Auth, setup the ldap server
#AUTH_LDAP_SERVER = "ldap://ldapserver.new"

# Uncomment to setup OpenID providers example for OpenID authentication
#OPENID_PROVIDERS = [
#    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
#    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
#    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
#    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
#---------------------------------------------------
# Babel config for translations
#---------------------------------------------------
# Setup default language
BABEL_DEFAULT_LOCALE = 'en'
# Your application default translation path
BABEL_DEFAULT_FOLDER = 'translations'
# The allowed translation for you app
LANGUAGES = {
	'en': {'flag':'gb', 'name':'English'},
	'pt': {'flag':'pt', 'name':'Portuguese'},
	'pt_BR': {'flag':'br', 'name': 'Pt Brazil'},
	'es': {'flag':'es', 'name':'Spanish'},
	'de': {'flag':'de', 'name':'German'},
	'zh': {'flag':'cn', 'name':'Chinese'},
	'ru': {'flag':'ru', 'name':'Russian'},
	'pl': {'flag':'pl', 'name':'Polish'}
}
#---------------------------------------------------
# Image and file configuration
#---------------------------------------------------
# The file upload folder, when using models with files
UPLOAD_FOLDER = basedir + '/app/static/uploads/'

# The image upload folder, when using models with images
IMG_UPLOAD_FOLDER = basedir + '/app/static/uploads/'

# The image upload url, when using models with images
IMG_UPLOAD_URL = '/static/uploads/'
# Setup image size default is (300, 200, True)
#IMG_SIZE = (300, 200, True)

# Theme configuration
# these are located on static/appbuilder/css/themes
# you can create your own and easily use them placing them on the same dir structure to override
#APP_THEME = "bootstrap-theme.css"  # default bootstrap
#APP_THEME = "cerulean.css"
#APP_THEME = "amelia.css"
#APP_THEME = "cosmo.css"
#APP_THEME = "cyborg.css"  
#APP_THEME = "flatly.css"
#APP_THEME = "journal.css"
APP_THEME = "readable.css"
#APP_THEME = "simplex.css"
#APP_THEME = "slate.css"   
#APP_THEME = "spacelab.css"
#APP_THEME = "united.css"
#APP_THEME = "yeti.css"

