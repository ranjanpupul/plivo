import base64
import hmac
from hashlib import sha1

import requests

try:
    import json
except ImportError:
    import simplejson as json

try:
    from urlparse import urlparse, parse_qsl, urljoin
except ImportError:
    # For Python 3
    from urllib.parse import urlparse, parse_qsl, urljoin

PLIVO_VERSION = "v1"


class PlivoError(Exception):
    pass



class PlivoAPI(object):
    def __init__(self, auth_id, auth_token, url='https://api.plivo.com', version=PLIVO_VERSION):
        self.version = version
        self.url = url.rstrip('/') + '/' + self.version
        self.auth_id = auth_id
        self.auth_token = auth_token
        self._api = self.url + '/Account/%s' % self.auth_id
        self.headers = {'User-Agent':'PythonPlivo'}

    def _request(self, method, path, data={}):
        path = path.rstrip('/') + '/'
        if method == 'POST':
            headers = {'content-type': 'application/json'}
            headers.update(self.headers)
            r = requests.post(self._api + path, headers=headers,
                              auth=(self.auth_id, self.auth_token),
                              data=json.dumps(data))
        elif method == 'GET':
            r = requests.get(self._api + path, headers=self.headers,
                             auth=(self.auth_id, self.auth_token),
                             params=data)
        elif method == 'DELETE':
            r = requests.delete(self._api + path, headers=self.headers,
                                auth=(self.auth_id, self.auth_token),
                                params=data)
        elif method == 'PUT':
            headers = {'content-type': 'application/json'}
            headers.update(self.headers)
            r = requests.put(self._api + path, headers=headers,
                             auth=(self.auth_id, self.auth_token),
                             data=json.dumps(data))
        content = r.content
        if content:
            try:
                response = json.loads(content.decode("utf-8"))
            except ValueError:
                response = content
        else:
            response = content
        return (r.status_code, response)

    @staticmethod
    def get_param(params, key):
        try:
            return params[key]
        except KeyError:
            raise PlivoError("missing mandatory parameter %s" % key)


    ## Message ##
    def send_message(self, params=None):
        if not params: params = {}
        return self._request('POST', '/Message/', data=params)

    def get_messages(self, params=None):
        if not params: params = {}
        return self._request('GET', '/Message/', data=params)

    def get_message(self, params=None):
        if not params: params = {}
        message_uuid = params.pop('message_uuid')
        return self._request('GET', '/Message/%s/' % message_uuid, data=params)


class PlivoResponse(object):
    def __init__(self, rest_api=None, response=None):
        "Create a response class from json and httpresponse"
        if response:
            self.status_code = response[0]
            self.json_data = response[1]
        if rest_api:
            self.rest_api = rest_api

    @classmethod
    def get_objects_from_response(cls, rest_api=None, response=None):
        objects = response[1]['objects']
        return_objects = []
        for obj in objects:
           response_tuple = (response[0], obj)
           return_objects.append(cls(response=response_tuple, rest_api=rest_api))
        return return_objects

    def __getattr__(self, k):
        if k in self.json_data:
            return self.json_data[k]
        else:
            raise AttributeError(k)

    def __repr__(self):
        return "Status: %s \nData: %s"%(self.status_code, self.json_data)


class Application(PlivoResponse):

    def create(self, app_name, answer_url, **optional_params):
        '''create an application'''
        optional_params.update({
            'app_name': app_name,
            'answer_url': answer_url,
        })
        return Application(response=self.rest_api.create_application(optional_params),
                           rest_api=self.rest_api)

    def get(self, app_id=None, **optional_params):
        ''' get details of an application'''
        if not app_id:
            app_id = self.app_id
        optional_params['app_id'] = app_id
        return Application(response=self.rest_api.get_application(optional_params),
                           rest_api=self.rest_api)

    def get_all(self, **optional_params):
        ''' get details of all applications '''
        return Application.get_objects_from_response(
            response=self.rest_api.get_applications(optional_params),
                rest_api=self.rest_api
            )

    def modify(self, app_id=None, **optional_params):
        ''' Modify an application '''
        if not app_id:
            app_id = self.app_id
        optional_params['app_id'] = app_id
        return Application(response=self.rest_api.modify_application(optional_params),
                           rest_api=self.rest_api)

    def delete(self, app_id=None, **optional_params):
        ''' Delete an application '''
        if not app_id:
            app_id = self.app_id
        optional_params['app_id'] = app_id
        return Application(response=self.rest_api.delete_application(optional_params),
                           rest_api=self.rest_api)


class Message(PlivoResponse):

    def send(self, src, dst, text, url, message_type="sms", method="POST", **optional_params):
        optional_params.update({
                'src': src,
                'dst': dst,
                'text': text,
                'type': message_type,
                'url': url,
                'method': method,
            })
        return Message(response=self.rest_api.send_message(optional_params),
                       rest_api=self.rest_api)

    def get(self, message_uuid=None, **optional_params):
        if not message_uuid:
            if type(self.message_uuid) == list:
                message_uuid = self.message_uuid[0]
            else:
                message_uuid = self.message_uuid

        optional_params['message_uuid'] = message_uuid
        return Message(response=self.rest_api.get_message(optional_params),
                       rest_api=self.rest_api)

    def get_all(self, **optional_params):
        return Message.get_objects_from_response(
            response=self.rest_api.get_messages(optional_params),
            rest_api=self.rest_api
        )
