from django.conf.urls import include, url
from plivoapp.views import SendMessage


urlpatterns = [
    url(r'^statusmessage', SendMessage.as_view()),
]
