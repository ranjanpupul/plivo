# -*- coding: utf-8 -*-
from django.shortcuts import render
import plivo
import json


def sendmessage(request):
    context={}
    auth_id = "MANTDLYTBLNWI5M2M1ZT"
    auth_token = "MDUyYzJhOWJiN2NiZmQ5NjYyM2MwYWVhMTAwYmU4"
    status = plivo.PlivoAPI(auth_id, auth_token)
    params = {
              'src': '17853290977',
              'dst': '15402531896',
              'text': u"Hello, how are you?",
              'url': "http://example.com/report/",
              'method': "POST",
              }

    response = status.send_message(params)
    context['message_uuid'] = (response[1]['message_uuid'])
    context['api_id'] = (response[1]['api_id'])
    responses = status.get_messages()
    context['value'] = responses[1]['objects']
    context['APIStatus'] = responses[0]
    return render(request, "result.html", context)