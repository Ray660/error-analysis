from django.urls import path
from . import views
from .views import *

app_name = 'user'
urlpatterns = [
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('personal_center', views.personal_view, name='personal')
]
