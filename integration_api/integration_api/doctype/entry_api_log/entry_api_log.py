# Copyright (c) 2025, ahmedatef and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class EntryApiLog(Document):
	def autoname(self):
		self.name = make_autoname(f"Ent-Log-.#####")

