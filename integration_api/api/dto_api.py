
import frappe
from ..Validations.request_validations import RequestValidation
from ..Validations.response_validations import Response




@frappe.whitelist()
def get_dto():
    validation_object = RequestValidation("Data Transfer Object")
    validation_object.validate_method()
    validation_object.validate_params()
    validation_object.validate_dto()
    query_params = validation_object.get_query_params()
    response = Response(query_params)
    response.get_response()








