from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

app_name='accounts'
urlpatterns=[
path('signup',views.signup_user,name='signup'),
path('login',views.login_user,name='login'),
path('logout',views.logout_user,name='logout'),
path('customersignup',views.customer_signup_view,name='customersignup'),
path('customerhome',views.customer_home_view,name='customerhome'),
path('adminbaner',views.admin_baner_view,name='adminbaner'),
path('afterlogin', views.afterlogin_view,name='afterlogin'),
path('customerprofileview',views.customer_profile_view,name='customerprofileview'),
path('editcustomerprofile',views.customer_profile_edit,name='editcustomerprofile'),
path('showadminprofile',views.admin_home_view,name='showadminprofile'),
path('editadminprofile',views.admin_edit_profile,name='editadminprofile'),
path('allcustomers',views.show_all_customer,name='allcustomers'),
path('deletecustomer/<int:ck>',views.delete_special_customer,name='deletecustomer'),
path('customerlogin', LoginView.as_view(template_name='accounts/customerlogin.html'),name='customerlogin'),
]
