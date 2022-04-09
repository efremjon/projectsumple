from django.urls import path,include
from .import views
urlpatterns = [
  


    path('',views.home,name='home'),

    ###############
    path('signup/',views.register,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),

    #########
    path('customer-dashbord/',views.Customer_page,name='customer_page'),
    #path('agent-dashbord/',views.Agent_page,name='agent-dashbord'),
    path('admin-dashbord/',views.Admin_page,name='admin-dashbord'),
    #########
]
