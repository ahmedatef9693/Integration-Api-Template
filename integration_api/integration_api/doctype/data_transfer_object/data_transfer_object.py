# Copyright (c) 2025, ahmedatef and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DataTransferObject(Document):
	@frappe.whitelist()
	def update_integration_fields(self):
		if self.integration_doctype:
			current_doctype = frappe.qb.DocType("DocField")
			query = frappe.qb.from_(current_doctype).\
				select(current_doctype.fieldname,current_doctype.fieldtype).\
				where(
					(current_doctype.parenttype == "DocType") 
					&
					(current_doctype.parent == self.integration_doctype)
					&
					(current_doctype.fieldtype.notin(["Column Break","Section Break"]))
		  	)
			data = query.run(as_dict=True)
			self.query_data = data
			self.table_name = "integration_fields"
			self.clear_table(self.table_name)
			self.add_fields(self.table_name)
			# self.save()
	def clear_table(self,table_name):
		self.set(table_name,[])

	def add_fields(self,table_name):
		for item in self.query_data:
			self.append(table_name,{
				"field_name":item.get("fieldname"),
				"field_type":item.get("fieldtype")
			})
		return "cleared"