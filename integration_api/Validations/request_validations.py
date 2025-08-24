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
            if (not key in fields) and (key != "page") :
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
        self.args = dict(frappe.local.request.args)
    
    def validate_page(self):
        # self.args = dict(self.request.args)
        if "page" not in self.args:
            self.args["page"] = 1
        else:
            page = int(self.args["page"])
            if page == 0:
                message = "Page Must Be Greater Than 0"
                frappe.local.response["message"] = message
                frappe.throw(message)

    def get_current_request(self):
        return self.args
    def validate_dto_existence(self):
        args_copy = deepcopy(self.args)
        if "page" in args_copy:
            args_copy.pop("page")
        self.validate_meta_data(args_copy)
        return True
    
