import json
import frappe
from integration_api.api.validations import UserValidation


@frappe.whitelist()
def create_entries(data_object):
    try:
        data_object = json.loads(data_object)
        token_validate = UserValidation()
        is_data_object_list(data_object)
        log_doc_name = create_log()
        create_entries_list(data_object,log_doc_name)
        
    
    except frappe.AuthenticationError as ae:
        frappe.local.response.http_status_code = 401
        frappe.local.response["message"] = str(ae)

    except frappe.ValidationError as ve:
        frappe.local.response.http_status_code = 422
        frappe.local.response["message"] = str(ve)

    except Exception as e:
        frappe.local.response.http_status_code = 404
        frappe.local.response["message"] = str(e)



def create_entries_list(data_object_list,log_doc_name):
    data_object_list_length = len(data_object_list)
    time_out = data_object_list_length * 10
    current_enqueue = frappe.enqueue(
                schedule_entry_list,
                queue='long',
                timeout=time_out,
                job_id="schedule_entry_list",
                event="Cron",
                readings = data_object_list,
                log_name = log_doc_name
            )
    frappe.local.response["message"] = f"Processing Request...{data_object_list_length}"

def is_data_object_list(readings):
    if not isinstance(readings, list):
        error_msg = "Entry Object Must Be List!"
        frappe.local.response["message"] = error_msg
        raise frappe.ValidationError(error_msg)

def schedule_entry_list(readings,log_name):
    log_doc = frappe.get_doc("Entry Api Log", log_name)
    for reading in readings:
        try:
            entry_doc = frappe.new_doc('Entry')
            entry_doc.update({
                "entry_name":reading.get('name'),
            })
            entry_doc.insert()
            log_doc.append("entry_log_details", {
                "transaction_code": entry_doc.get("name"),
                "status_message": "Accepted"
            })
        except frappe.ValidationError as ve:
            frappe.log_error(str(ve))
            log_doc.append("entry_log_details", {
                "transaction_code": entry_doc.get("name"),
                "status_message":"Exception",
                "error_description": str(ve)
            })
        except Exception as e:
            frappe.log_error(str(e))
            log_doc.append("entry_log_details", {
                "transaction_code": entry_doc.get("name"),
                "status_message":"Exception",
                "error_description": str(e)
            })
    log_doc.save()
    frappe.db.commit()



def create_log():
    log_doc = frappe.get_doc({
            "doctype": "Entry Api Log",
            "entry_log_details": [],
        })
    log_doc.insert()
    return log_doc.name
    