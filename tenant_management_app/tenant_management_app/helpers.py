from datetime import datetime

import frappe


def validate_single_data(*args):
    for arg in args:
        if len(arg.split(' ')) > 1:
            return frappe.throw(f"'{arg}' is invalid")


def clean_data(self, **kwargs):
    for k, w in kwargs.items():
        if getattr(self, k) is not None:
            if len(w.split()) > 1:
                setattr(self, k, w.title())
            else:
                setattr(self, k, w.capitalize())


def get_agent():
    agent = frappe.db.exists(
        "Agent",
        {
            "email": frappe.session.user,
        }
    )
    return agent


def get_house_owner():
    house_owner = frappe.db.exists(
        "House Owner",
        {
            "email": frappe.session.user,
        }
    )
    return house_owner


def convert_to_date_object(date_string):
    date_format = '%Y-%m-%d'
    date_object = datetime.strptime(date_string, date_format).date()
    return date_object


def get_user_by_email(email):
    if 'Administrator' in frappe.get_roles():
        user = frappe.get_doc("User", {"username": email.lower()})
    else:
        user = frappe.get_doc("User", {"email": email})
    print(89080, user)
    return user
