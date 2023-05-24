# Copyright (c) 2023, Akinola Marvellous and contributors
# For license information, please see license.txt

import frappe

# from frappe.model.docstatus import DocStatus
from frappe.model.document import Document
from tenant_management_app.tenant_management_app.helpers import validate_single_data, clean_data, get_agent


class Tenant(Document):
    def before_save(self):
        self.validate_house_availability()
        if 'House Agent' in frappe.get_roles():
            self.agent = get_agent()
        validate_single_data(self.first_name, self.last_name)
        clean_data(self, first_name=self.first_name, last_name=self.last_name, occupation=self.occupation)

    def validate_house_availability(self):
        house = frappe.get_doc("House", self.house)
        if house.status == "Unavailable":
            frappe.throw("Selected House is already occupied")
        house.status = "Unavailable"
        house.save()
