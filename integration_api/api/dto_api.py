import frappe





@frappe.whitelist()
def get_dto():
    validation_object = RequestValidation("Data Transfer Object")
    validation_object.validate_method()
    validation_object.validate_params()
    validation_object.validate_dto()
    query_params = validation_object.get_query_params()
    response = Response(query_params)
    response.get_response()



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
        

    



class Response:
    def __init__(self,query_params):
        self.query_params = query_params
        self.integration_doctype = self.query_params.get("integration_doctype")
    
    def get_response(self):
        query = self.get_dto_with_fields()
        integration_fields = []
        for item in query:
            integration_fields.append({
                "fieldname":item.get("field_name"),
                "fieldtype":item.get("field_type")
                })
        self.response = {   
            "status": "Success",
            "message": "Data Transfer Object Fetched Successfully",
            "integration_doctype": self.integration_doctype,
            "integration_fields": integration_fields
            }
    
        frappe.local.response["status"] = self.response["status"]
        frappe.local.response["message"] = self.response["message"]
        frappe.local.response["integration_doctype"] = self.response["integration_doctype"]
        frappe.local.response["integration_fields"] = self.response["integration_fields"]
    
    def get_dto_with_fields(self):
        integration_details = frappe.qb.DocType("Integration Fields Details")
        doctype = frappe.qb.DocType("Data Transfer Object")
        return frappe.qb.from_(doctype)\
            .inner_join(integration_details)\
            .on(doctype.name == integration_details.parent)\
            .select(
                doctype.integration_doctype,
                integration_details.field_name,
                integration_details.field_type
                ).\
            where(
                (doctype.integration_doctype == self.integration_doctype)
                &
                (integration_details.include == 1)
                ).run(as_dict=True)

        



class NotFoundException(Exception):
    http_status_code = 404

    def __init__(self, message="Function Method Not Found", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message
