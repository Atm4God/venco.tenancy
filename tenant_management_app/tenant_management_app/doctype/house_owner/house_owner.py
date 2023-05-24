# Copyright (c) 2023, Akinola Marvellous and contributors
# For license information, please see license.txt

import frappe
# from frappe.model.docstatus import DocStatus
from frappe.model.document import Document
from tenant_management_app.tenant_management_app.helpers import get_user_by_email


class HouseOwner(Document):
	def before_save(self):
		user_email = frappe.session.user
		house_owner = frappe.db.exists(
			"House Owner",
			{
				"email": user_email,
				# "docstatus": DocStatus.submitted(),
			},
		)
		if house_owner:
			frappe.throw("You are already a house owner")
		user_email = frappe.session.user
		user = get_user_by_email(user_email)
		self.email = user_email
		self.full_name = f'{user.first_name} {user.last_name}'
