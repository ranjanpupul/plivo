# -*- coding: utf-8 -*-
from django.shortcuts import render
import plivo
import json
from forms import UserExitForm
from django.views.generic import View
from django.contrib import messages

class PostMessage(View):
    def get(self, request):
        try:

           	context = {"form": "", "concent": ""}
           	form = UserExitForm() 
           	context["form"] = form
        	auth_id = "MANTDLYTBLNWI5M2M1ZT"
    		auth_token = "MDUyYzJhOWJiN2NiZmQ5NjYyM2MwYWVhMTAwYmU4"
    		status = plivo.PlivoAPI(auth_id, auth_token)
    		responses = status.get_messages()
    		context['value'] = responses[1]['objects']
    		context['APIStatus'] = responses[0]
    		return render(request, "result.html", context)          
           
        except Exception as programmingerror:
        	context = {"form": ""}
        	form = UserExitForm()
        	context["form"] = form
        	return render(request, "result.html", context)

    def post(self, request):
        context = {"form": ""}
        form = UserExitForm(request.POST)
        if form.is_valid():
            try:
                tonumber = form.cleaned_data['tonumber']
                fromnumber = form.cleaned_data['fromnumber']
                message = form.cleaned_data['message']
                auth_id = "MANTDLYTBLNWI5M2M1ZT"
                auth_token = "MDUyYzJhOWJiN2NiZmQ5NjYyM2MwYWVhMTAwYmU4"
                status = plivo.PlivoAPI(auth_id, auth_token)
                params = {'src': tonumber, 'dst': fromnumber, 'text': 'u'+message, 'url': "http://example.com/report/", 'method': "POST", }
                response = status.send_message(params)
                if response[1]['error']:
                	context['error']= response[1]['error']
                	context['code']= response[0]
                	messages.error(request, 'oops   something went wrong')
                	context['form']  = UserExitForm()
                	return render(request, "result.html", context)
                context['message_uuid'] = (response[1]['message_uuid'])
                context['api_id'] = (response[1]['api_id'])
                responses = status.get_messages()
                context['value'] = responses[1]['objects']
                context['APIStatus'] = responses[0]
                context['form']  = UserExitForm()
                return render(request, 'result.html', context)
            except Exception as e:
               	print e
        return render(request, "result.html", context)