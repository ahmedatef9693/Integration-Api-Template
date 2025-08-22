
import frappe
from ..Validations.request_validations import ResourceValidation




@frappe.whitelist()
def get_resource():
    request_validation = ResourceValidation("Data Transfer Object")
    request_validation.validate_method()
    request_validation.validate_limit()
    request_validation.validate_dto_existence()
    current_request = request_validation.get_current_request()
    get_dto_fields(current_request)



def get_dto_fields(args):
    start,limit = get_limits(args)
    d = frappe.get_doc("Data Transfer Object",args)
    dto_fields_list = []
    for item in d.integration_fields:
        if item.include:
            dto_fields_list.append(item.field_name)
    selection_fields = " ,".join(dto_fields_list).replace("'","")
    integration_doctype = str(frappe.qb.DocType(args.get("integration_doctype"))).replace('"','`')
    query = f"""Select {selection_fields} from {integration_doctype} limit {start},{limit}"""
    q = frappe.db.sql(query,as_dict=True)
    frappe.local.response["status"] = "Success"
    frappe.local.response["message"] = "Data Transfer Object Fetched Successfully"
    frappe.local.response["integration_doctype"] = args.get("integration_doctype")
    frappe.local.response["integration_fields"] = dto_fields_list
    frappe.local.response["data"] = q


def get_limits(args):
    start = args.get("start")
    args.pop("start")
    limit = args.get("limit")
    args.pop("limit")
    return start,limit