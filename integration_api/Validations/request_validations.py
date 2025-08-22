# .Exceptions.errors_handling import NotFoundException
from ..Exceptions.errors_handling import NotFoundException
import frappe
from copy import deepcopy
class RequestValidation:
    def __init__(self,doctype_name):
        self.doctype_name = doctype_name 
        self.request = frappe.local.request
    def validate_method(self):
        if self.request.method != "GET":
            raise NotFoundException("Function Method Not Found")
    def validate_meta_data(self,params):
        meta_data = frappe.get_meta(self.doctype_name)
        fields = [
            field.fieldname for field in meta_data.fields
        ]
        for i, key in enumerate(params.keys()):
            if (not key in fields) and (key != "start") and (key != "limit"):
                frappe.throw(f'Field {key} Doesnt Exists In Data Transfer Object')


    





class DTORequestValidation(RequestValidation):
    def __init__(self,doctype_name):
        super().__init__(doctype_name)
    

    def validate_params(self):
        self.query_params = dict(self.request.args)
        self.validate_meta_data(self.query_params)
    def validate_dto(self):
        if not frappe.db.exists(self.doctype_name,self.query_params):
            raise NotFoundException(f"Query Params Error")
    
    def get_query_params(self):
        return self.query_params




class ResourceValidation(RequestValidation):
    def __init__(self,doctype_name):
        super().__init__(doctype_name)
    
    def validate_limit(self):
        self.args = dict(self.request.args)
        if "start" not in self.args:
            self.args["start"] = 0
        if "limit" not in self.args:
            self.args["limit"] = 5

    def get_current_request(self):
        return self.args
    def validate_dto_existence(self):
        args_copy = deepcopy(self.args)
        if "start" in args_copy:
            args_copy.pop("start")
        if "limit" in args_copy:
            args_copy.pop("limit")
        self.validate_meta_data(args_copy)
        return True
    
