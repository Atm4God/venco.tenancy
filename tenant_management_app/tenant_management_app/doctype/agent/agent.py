# Copyright (c) 2023, Akinola Marvellous and contributors
# For license information, please see license.txt

import frappe
# from frappe.model.docstatus import DocStatus
from frappe.model.document import Document
from datetime import datetime

from tenant_management_app.tenant_management_app.helpers import get_user_by_email


class Agent(Document):
	def before_save(self):
		self.date_joined = datetime.now()

		user_email = frappe.session.user
		agent = frappe.db.exists(
			"Agent",
			{
				"email": user_email,
				# "docstatus": DocStatus.submitted(),
			},
		)
		if agent:
			frappe.throw("You are already a house owner")
		self.email = user_email
