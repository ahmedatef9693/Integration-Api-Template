# .Exceptions.errors_handling import NotFoundException
from ..Exceptions.errors_handling import NotFoundException
import frappe

class RequestValidation:
    def __init__(self,doctype_name):
        self.doctype_name = doctype_name 
        self.request = frappe.local.request
    def validate_method(self):
        if self.request.method != "GET":
            raise NotFoundException("Function Method Not Found")

    def validate_params(self):
        self.query_params = dict(self.request.args)
        self.validate_meta_data(self.query_params)
    def validate_dto(self):
        if not frappe.db.exists(self.doctype_name,self.query_params):
            raise NotFoundException(f"Query Params Error")
        


    def validate_meta_data(self,params):
        meta_data = frappe.get_meta(self.doctype_name)
        fields = [
            field.fieldname for field in meta_data.fields
        ]
        for i, key in enumerate(params.keys()):
            if not key in fields:
                frappe.throw(f'Field {key} Doesnt Exists In Data Trasnfer Object')

    def get_query_params(self):
        return self.query_params