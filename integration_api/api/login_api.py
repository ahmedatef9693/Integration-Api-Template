from integration_api.api.validations import UserValidation
import frappe
from frappe import _
from frappe.core.doctype.user.user import generate_keys
from integration_api.api.constants import *
import json

@frappe.whitelist(allow_guest=True)
def login(email, password):

    user = frappe.get_all('User', filters={'email': email}, fields=['name', 'enabled'])
    if not user:
        return {"message": _("User not found"), "status": "fail"}

    user = user[0]
    if not user.get('enabled'):
        return {"message": _("User is disabled"), "status": "fail"}
   

    try:
        login_manager = frappe.local.login_manager
        login_manager.authenticate(email, password)
        login_manager.post_login()
        token_validate = UserValidation(email=email)
        response_cached_value = token_validate.validate_cache_and_get()

        if response_cached_value:
            return response_cached_value
        else:
            api_secret = generate_keys(user['name']).get('api_secret', '')
            user_doc = frappe.get_cached_doc('User', user['name'])

            response = {
                "message": _("Login successful"),
                "status": "Success",
                "api_key": user_doc.api_key,
                "api_secret": api_secret,
            }

            token_validate.set_cache(email,response)
            session_id = frappe.local.session.get("sid")
            if session_id:
                frappe.db.delete("Sessions", {"sid": session_id})
                frappe.db.commit()

            return response

    except frappe.exceptions.AuthenticationError:
        return {"message": _("Invalid credentials"), "status": "fail"}



