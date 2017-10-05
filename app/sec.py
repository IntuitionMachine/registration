from flask_appbuilder.security.sqla.manager import SecurityManager
from .models import MyUser
from .sec_views import MyUserDBModelView,MyUserInfoEditView,MyRegisterUserDBView,MyAuthDBView,MyUserStatsChartView
#from .sec_forms import UserInfoEdit
#from flask_appbuilder.security.views import UserInfoEditView
#from .registration import MyRegisterUserDBView

#class MyUserInfoEditView(UserInfoEditView):
#    form = UserInfoEdit
class MySecurityManager(SecurityManager):
    user_model = MyUser    			#Extend default user model
    #registeruserdbview = MyRegisterUserDBView		#override register view
    userdbmodelview = MyUserDBModelView				#override user db model view (i.e Show User)
    userinfoeditview = MyUserInfoEditView			#override user's self edit view
    authdbview = MyAuthDBView
    #userdbmodelview = MyUserDBModelView
    #userinfoeditview = MyUserInfoEditView
    userstatschartview=MyUserStatsChartView