from django.urls import path
from . import views
from .views import *

app_name = 'interact'
urlpatterns = [
    path('topic_input', views.topic_input, name='topic_input'),
]
