import frappe
import json
import hashlib

from integration_api.api.constants import *

class UserValidation:
    def __init__(self,email=None):
        self.user = email
        if (not self.user):
            self.validate_user_token()



    def validate_user_token(self):
        cached_value = self.validate_cache_and_get()
        if not cached_value:
            raise frappe.AuthenticationError('Invalid Credentials.Token Expired Please Try Logging In Again.')
        else:
            token = str(frappe.local.request.headers['Authorization'])
            token = token.replace("token ", "").split(':')
            if cached_value.get('api_key') != token[0]:
                raise frappe.AuthenticationError('Invalid Credentials Api Key Error!')
            
            if cached_value.get('api_secret') != token[1]:
                raise frappe.AuthenticationError('Invalid Credentials Api Secret Error!')
    

    def validate_cache_and_get(self):
        if not self.user:
            self.user = frappe.session.user
        
        key = hashlib.sha256(f"{self.user}".encode()).hexdigest()
        cached_response = frappe.cache().get(key)
        cached_response = frappe.safe_decode(cached_response)
        if cached_response:
            return json.loads(cached_response)
        else:
            return None
    def set_cache(self,email,response):
        key = hashlib.sha256(f"{email}".encode()).hexdigest()
        frappe.cache().setex(key,TOKEN_EXPIRY_TIME,json.dumps(response))