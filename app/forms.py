from wtforms import Form, StringField,IntegerField,DateField,validators,PasswordField,SelectField
from wtforms.validators import DataRequired,EqualTo,Email
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget,BS3PasswordFieldWidget,DatePickerWidget,Select2Widget
from flask_babel import lazy_gettext
from flask_wtf.recaptcha import RecaptchaField

class TweetForm(DynamicForm):
	message=StringField(lazy_gettext('Tweet Message'),validators=[DataRequired()],widget=BS3TextFieldWidget())

class ProfileForm(DynamicForm):
	id = IntegerField(('id'))
	fname = StringField(('fname'),description=('First Name'),validators = [DataRequired()], widget=BS3TextFieldWidget())
	lname = StringField(('lname'),description=('Last Name'), widget=BS3TextFieldWidget())
	email = StringField(('email'),description=('Last Name'), widget=BS3TextFieldWidget())
	#birthday=DateField("birthday", format='%Y/%m/%d', widget=DatePickerWidget())
	streetAddress=StringField("streetAddress", [validators.DataRequired()])
	country=StringField("country", [validators.DataRequired()])
	city=StringField("city", [validators.Length(min=4, max=25)])
	state=StringField("state", [validators.Length(min=4, max=25)])
	zipCode=StringField("zipCode", [validators.Length(min=4, max=25)])
	ethereumAddress=StringField("ethereumAddress", [validators.DataRequired()])
	govID=StringField("govID", [validators.Length(min=4, max=25)])

class MyUserInfoEdit(DynamicForm):
	username = StringField(lazy_gettext('User Name'), validators=[DataRequired()], widget=BS3TextFieldWidget())
	first_name = StringField("First Name", widget=BS3TextFieldWidget())
	last_name = StringField("Last Name", widget=BS3TextFieldWidget())
	email = StringField("Email", widget=BS3TextFieldWidget())
	birthday=DateField("Birthday", widget=DatePickerWidget())
	streetAddress=StringField("Address", [validators.DataRequired()], widget=BS3TextFieldWidget())
	city=StringField("City", [validators.Length(min=4, max=25)], widget=BS3TextFieldWidget())
	state=StringField("State", [validators.Length(min=4, max=25)], widget=BS3TextFieldWidget())
	zipCode=StringField("Zip Code", [validators.Length(min=4, max=25)], widget=BS3TextFieldWidget())
	ethAddress=StringField("Ethereum Address", [validators.DataRequired()], widget=BS3TextFieldWidget())
	govID=StringField("Government ID", [validators.Length(min=4, max=25)], widget=BS3TextFieldWidget())
	#geoIP=StringField("IP", widget=BS3TextFieldWidget())
	#geoLoc = StringField("Geo-Location", widget=BS3TextFieldWidget())
	country=SelectField("Country",widget=Select2Widget(),choices=[('AF','Afghanistan'),('AL','Albania'),('DZ','Algeria'),('AS','American Samoa'),('AD','Andorra'),('AO','Angola'),('AI','Anguilla'),('AQ','Antarctica'),('AG','Antigua and Barbuda'),('AR','Argentina'),('AM','Armenia'),('AW','Aruba'),('AU','Australia'),('AT','Austria'),('AZ','Azerbaijan'),('BS','Bahamas'),('BH','Bahrain'),('BD','Bangladesh'),('BB','Barbados'),('BY','Belarus'),('BE','Belgium'),('BZ','Belize'),('BJ','Benin'),('BM','Bermuda'),('BT','Bhutan'),('BO','Bolivia'),('BA','Bosnia and Herzegovina'),('BW','Botswana'),('BV','Bouvet Island'),('BR','Brazil'),('BQ','British Antarctic Territory'),('IO','British Indian Ocean Territory')])
class MyRegisterUserDBForm(DynamicForm):
	username = StringField(lazy_gettext('User Name'), validators=[DataRequired()], widget=BS3TextFieldWidget())
	first_name = StringField(lazy_gettext('First Name'), validators=[DataRequired()], widget=BS3TextFieldWidget())
	last_name = StringField(lazy_gettext('Last Name'), validators=[DataRequired()], widget=BS3TextFieldWidget())
	email = StringField(lazy_gettext('Email'), validators=[DataRequired()], widget=BS3TextFieldWidget())
	password = PasswordField(lazy_gettext('Password'),
							 description=lazy_gettext(
								 'Please use a good password policy, this application does not check this for you'),
							 validators=[DataRequired()],
							 widget=BS3PasswordFieldWidget())
	conf_password = PasswordField(lazy_gettext('Confirm Password'),
								  description=lazy_gettext('Please rewrite the password to confirm'),
								  validators=[EqualTo('password', message=lazy_gettext('Passwords must match'))],
								  widget=BS3PasswordFieldWidget())
# birthday=DateField("Birthday", format='%Y/%m/%d', widget=DatePickerWidget())
# streetAddress=StringField("Address", [validators.DataRequired()], widget=BS3TextFieldWidget())
# country=StringField("Country", [validators.DataRequired()], widget=BS3TextFieldWidget())
# city=StringField("City", [validators.Length(min=4, max=25)], widget=BS3TextFieldWidget())
# state=StringField("State", [validators.Length(min=4, max=25)], widget=BS3TextFieldWidget())
# zipCode=StringField("Zip Code", [validators.Length(min=4, max=25)], widget=BS3TextFieldWidget())
# ethAddress=StringField("Ethereum Address", [validators.DataRequired()], widget=BS3TextFieldWidget())
# govID=StringField("Government ID", [validators.Length(min=4, max=25)], widget=BS3TextFieldWidget())
# geoIP=StringField("IP", widget=BS3TextFieldWidget())
# geoLoc = StringField("Geo-Location", widget=BS3TextFieldWidget())
# country=SelectField("Country",widget=Select2Widget(),choices=[('AF','Afghanistan'),('AL','Albania'),('DZ','Algeria'),('AS','American Samoa'),('AD','Andorra'),('AO','Angola'),('AI','Anguilla'),('AQ','Antarctica'),('AG','Antigua and Barbuda'),('AR','Argentina'),('AM','Armenia'),('AW','Aruba'),('AU','Australia'),('AT','Austria'),('AZ','Azerbaijan'),('BS','Bahamas'),('BH','Bahrain'),('BD','Bangladesh'),('BB','Barbados'),('BY','Belarus'),('BE','Belgium'),('BZ','Belize'),('BJ','Benin'),('BM','Bermuda'),('BT','Bhutan'),('BO','Bolivia'),('BA','Bosnia and Herzegovina'),('BW','Botswana'),('BV','Bouvet Island'),('BR','Brazil'),('BQ','British Antarctic Territory'),('IO','British Indian Ocean Territory')])
recaptcha = RecaptchaField()