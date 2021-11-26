from django.urls import path
from . import views

urlpatterns = [
    # path('IMS/signup', views.signup, name='signup'),
    path('IMS/login', views.WMS_login, name='login'),
    path('IMS/logout', views.WMS_logout, name='logout'),
    path('IMS/change_password', views.change_password, name='change_password'),
]