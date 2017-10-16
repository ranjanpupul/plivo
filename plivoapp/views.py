from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect, HttpResponse ,JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

# Create your views here.
import requests
import json
 

class SendMessage(APIView):
	def get(self, request):
		context={}
		API_ENDPOINT = "https://api.plivo.com/v1/Account/**********/Message/"		 
		data = {'src':'17853290977',
		        'dst':'15402531896',
		        'text':'Hello heya it works'}
		headers = {'content-type': 'application/json'}
		data = json.dumps(data, ensure_ascii=False)
		# sending post request and saving response as response object
		try:
			r = requests.post(url = API_ENDPOINT, data = data, headers=headers)
		except exception as e:
			print e
		print r.status_code
		pastebin_url = r.text
		context['response'] = r.status_code
		print("The pastebin URL is:%s"%pastebin_url)
		return render(request, "result.html", context)