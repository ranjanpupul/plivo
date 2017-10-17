from django.conf.urls import include, url
from plivoapp.views import sendmessage


urlpatterns = [
    url(r'^statusmessage', sendmessage),
]
