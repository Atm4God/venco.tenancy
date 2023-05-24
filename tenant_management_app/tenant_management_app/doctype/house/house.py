# Copyright (c) 2023, Akinola Marvellous and contributors
# For license information, please see license.txt

import frappe
# from frappe.model.docstatus import DocStatus
from frappe.model.document import Document
from tenant_management_app.tenant_management_app.helpers import get_house_owner, get_user_by_email


class House(Document):
    def before_save(self):
        self.is_permitted()
        user_email = frappe.session.user

        house_owner = frappe.db.exists(
            "House Owner",
            {
                "email": user_email,
                # "docstatus": DocStatus.submitted(),
            },
        )
        if not house_owner:
            user = get_user_by_email(user_email)
            house_owner = frappe.new_doc('House Owner')

            house_owner.email = user_email
            house_owner.full_name = f"{user.first_name or ''} {user.last_name or ''}"
            house_owner.insert()
            house_owner = house_owner.name
        # else:
        #     house_owner = frappe.get_value("House Owner", {"email": user_email})
        self.house_owner = house_owner

    # def before_cancel(self):
    #     frappe.throw("Got here before")
    #
    #     if self.is_permitted():
    #         house_owner = get_house_owner()
    #         if self.house_owner != house_owner:
    #             frappe.throw("You cannot delete other users' houses!", PermissionError)
    #     frappe.throw("Unauthorized please!", PermissionError)

    @staticmethod
    def is_permitted():
        user_roles = frappe.get_roles()
        print("user roles", user_roles)
        if "House Owner" not in user_roles:
            print("Please")
            frappe.throw("You're  not permitted to perform this action")
        else: print("You're allowed to perform this action'")
