from django.conf.urls import re_path, url
from . import views

app_name = 'messenger_bot'
urlpatterns = [re_path('^$', views.new_message_received, name='new_message')]
