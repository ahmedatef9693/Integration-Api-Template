
import frappe
from ..Validations.request_validations import ResourceValidation




@frappe.whitelist()
def get_resource():
    request_validation = ResourceValidation("Data Transfer Object")
    request_validation.validate_method()
    request_validation.validate_page()
    request_validation.validate_dto_existence()
    current_request = request_validation.get_current_request()
    get_dto_fields(current_request)



def get_dto_fields(args):
    page = args.get("page")
    args.pop("page")
    integration_doctype = args.get("integration_doctype")
    start,limit ,page_size,total_number_of_pages = make_page(0,0,page,integration_doctype)
    dto_doc = frappe.get_doc("Data Transfer Object",args)
    dto_fields_list = []
    for item in dto_doc.integration_fields:
        if item.include:
            dto_fields_list.append(item.field_name)
    doctype = frappe.qb.DocType(integration_doctype)
    q = (
        frappe.qb.from_(doctype)
        .select(*dto_fields_list)
        .limit(page_size)
        .offset(start)
    )
    results = q.run(as_dict=True)
    build_success_response(start=start,limit=limit,page_size=page_size,total_number_of_pages=total_number_of_pages,page=page,dto_fields_list=dto_fields_list,results=results,integration_doctype=integration_doctype)



def make_page(start,limit,page,integration_doctype):
    import math
    page_size  = 5
    page = int(page)
    total_rows = frappe.db.count(f"{integration_doctype}")
    total_number_of_pages = max(1, math.ceil(total_rows / page_size))
    start = (page - 1) * (page_size)
    limit = min(start + page_size,total_rows)
    return start , limit , page_size,total_number_of_pages


def build_success_response(start,limit,page_size,integration_doctype,dto_fields_list,total_number_of_pages,page,results):
    frappe.local.response["status"] = "Success"
    frappe.local.response["message"] = "Data Transfer Object Fetched Successfully"
    frappe.local.response["integration_doctype"] = integration_doctype
    frappe.local.response["page_size"] = page_size
    frappe.local.response["total_number_of_pages"] = total_number_of_pages
    frappe.local.response["start"] = start
    frappe.local.response["limit"] = limit
    frappe.local.response["current_page"] = int(page)
    frappe.local.response["integration_fields"] = dto_fields_list
    frappe.local.response["data"] = results