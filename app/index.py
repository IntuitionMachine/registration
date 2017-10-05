#from .forms import UserForm
from flask_appbuilder import IndexView
from flask_appbuilder import expose
class MyIndexView(IndexView):
	route_base=''
	default_view='index'
	index_template='appbuilder/index.html'
	@expose('/')
	def index(self):
		print("HEY\n\n\n")
		return self.render_template(self.index_template)

