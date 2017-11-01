from django.conf.urls import include, url
from plivoapp.views import  PostMessage


urlpatterns = [
    url(r'^statusmessage', PostMessage.as_view()),
    
]
