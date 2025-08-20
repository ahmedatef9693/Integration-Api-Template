import frappe
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

        