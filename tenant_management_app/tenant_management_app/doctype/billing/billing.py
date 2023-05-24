# Copyright (c) 2023, Akinola Marvellous and contributors
# For license information, please see license.txt

import frappe
from datetime import date

# from frappe.model.docstatus import DocStatus
from frappe.website.website_generator import WebsiteGenerator
from tenant_management_app.tenant_management_app.helpers import convert_to_date_object, get_agent, get_house_owner


class Billing(WebsiteGenerator):
    def get_page_info(self):
        route = super().get_page_info()
        house = frappe.get_doc('House', self.house)
        tenant = frappe.get_doc('Tenant', self.tenant)
        route.house = house
        route.tenant = tenant

        return route
    # @property
    # def total_amount(self):
    #     print("problem is here")
    #     if self.house:
    #         house = frappe.get_doc('House', self.house)
    #         return (self.rent_amount or 0) + (house.security_fee or 0) + (self.agency_fee or 0)

    def before_save(self):
        self.user_can_create()
        self.verify_billing_existence()
        self.validate_payment_due_date()
        self.set_read_only_fields()

    def validate_payment_due_date(self):
        due_date = convert_to_date_object(self.payment_due_date)
        if due_date < date.today():
            frappe.throw("Invalid payment due date!")

    def verify_billing_existence(self):
        billing = frappe.get_list(
            "Billing",
            {
                "house": self.house,
                # "docstatus": DocStatus.submitted(),
            },
            order_by="creation DESC", limit=1
        )
        if billing:
            # tenant = frappe.get_doc("tenant", billing.tenant)
            active_agreement_exists = self.get_active_agreement()
            if active_agreement_exists:
                frappe.throw("There is an active agreement for this house")
            pass
        pass

    def get_active_agreement(self):
        agreement = frappe.get_list(
            "Rental Agreement",
            {
                "house": self.house,
                "is_active": True,
                # "docstatus": DocStatus.submitted(),
                "end_date": (">", date.today()),
            },
            order_by="creation DESC", limit=1
        )
        print(agreement)
        return agreement

    @staticmethod
    def user_has_role(role: str):
        user_roles = frappe.get_roles()
        return bool(role in user_roles)

    def user_can_create(self):
        is_agent = self.user_has_role("House Agent")
        is_owner = self.user_has_role("House Owner")
        agreement = frappe.get_doc("Rental Agreement", self.agreement)
        if is_agent:
            agent = get_agent()
            self.agent = agent
            if agreement.agent != agent:
                frappe.throw("Selected Agreement is not created by you!", PermissionError)
        elif is_owner:
            house_owner = get_house_owner()
            house = frappe.get_doc("House", agreement.house)
            if house.house_owner != house_owner:
                frappe.throw("Selected Agreement is not created by you!")
        pass

    def get_rent_type(self):
        house = frappe.get_doc("House", self.house)
        rent_type = house.rent_type
        return rent_type[:-2]

    def set_read_only_fields(self):
        agreement = frappe.get_doc("Rental Agreement", self.agreement)
        print(111, self.house)
        self.house = self.house or agreement.house
        self.tenant = self.tenant or agreement.tenant
        self.rental_period = f"{agreement.lease_term_count} {self.get_rent_type()} " \
                             f"{'s' if agreement.lease_term_count > 1 else ''}"
        self.route = self.name
        self.rent_amount = agreement.rent_amount
        house = frappe.get_doc('House', self.house)
        self.total_amount = (self.rent_amount or 0) + (house.security_fee or 0) + (self.agency_fee or 0)

























































