# Copyright (c) 2023, Akinola Marvellous and contributors
# For license information, please see license.txt
from datetime import date

import frappe
# from frappe.model.docstatus import DocStatus
from frappe.model.document import Document
from tenant_management_app.tenant_management_app.helpers import get_agent, get_house_owner, convert_to_date_object


class RentalAgreement(Document):
    def before_save(self):
        tenant = frappe.get_doc("Tenant", self.tenant)
        self.house = tenant.house
        self.validate_agreement()
        self.is_permitted(tenant)
        self.validate_start_date()
        house = frappe.get_doc("House", self.house)
        self.set_end_date(house)
        self.rent_amount = float(house.rent_amount) * self.lease_term_count

    def before_submit(self):
        self.validate_agreement()
        self.is_active = True

    def validate_agreement(self):
        agreement_exists = frappe.db.exists(
            "Rental Agreement",
            {
                "house": self.house,
                # "docstatus": DocStatus.submitted(),
                "end_date": (">", date.today()),
            }
        )
        if agreement_exists:
            frappe.throw("There is an active agreement for this house")

    def validate_start_date(self):
        start_date = convert_to_date_object(self.start_date)
        if start_date < date.today():
            frappe.throw("Invalid Start Date")

    def is_permitted(self, tenant):
        if 'House Agent' in frappe.get_roles():
            agent = get_agent()
            if tenant.agent != agent:
                frappe.throw("You cannot perform this action")
            self.agent = agent

        elif 'House Owner' in frappe.get_roles():
            owner = get_house_owner()
            house = frappe.db.exists(
                "House",
                {
                    "name": self.house,
                    "house_owner": owner,
                    # "docstatus": DocStatus.submitted(),
                }
            )
            if not house:
                frappe.throw("You cannot perform this action. Not your Tenant")

    def set_end_date(self, house):
        if house.rent_type == "Monthly":
            self.end_date = frappe.utils.add_months(self.start_date, self.lease_term_count or 1)
        else:
            self.end_date = frappe.utils.add_years(self.start_date, self.lease_term_count or 1)
