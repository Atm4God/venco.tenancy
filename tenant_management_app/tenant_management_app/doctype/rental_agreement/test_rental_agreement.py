# Copyright (c) 2023, Akinola Marvellous and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from tenant_management_app.tenant_management_app.doctype.rental_agreement.rental_agreement import RentalAgreement

import frappe
from datetime import date, timedelta
import unittest
from tenant_management_app.tenant_management_app.helpers import convert_to_date_object


class TestRentalAgreement(FrappeTestCase):
    def setUp(self):
        # Create test data if needed
        pass

    def tearDown(self):
        # Clean up test data if needed
        pass

    def test_validate_agreement(self):
        agreement = RentalAgreement()
        agreement.house = "Test House"
        # agreement.docstatus = 1
        agreement.end_date = date.today()

        # Existing active agreement should cause an exception
        with self.assertRaises(frappe.ValidationError):
            agreement.validate_agreement()

        # Non-existing active agreement should pass validation
        agreement.end_date = date.today() - timedelta(days=1)
        agreement.validate_agreement()

    def test_validate_start_date(self):
        agreement = RentalAgreement()
        agreement.start_date = "2023-05-01"

        # Invalid start date should cause an exception
        with self.assertRaises(frappe.ValidationError):
            agreement.validate_start_date()

        # Valid start date should pass validation
        agreement.start_date = "2023-06-01"
        agreement.validate_start_date()

    def test_is_permitted(self):
        agreement = RentalAgreement()

        # User with 'House Agent' role should be permitted
        frappe.set_user("agent@example.com")
        agreement.tenant = "Test Tenant"
        agreement.is_permitted(agreement.tenant)

        # User without 'House Agent' role should raise an exception
        frappe.set_user("random@example.com")
        agreement.tenant = "Test Tenant"
        with self.assertRaises(frappe.ValidationError):
            agreement.is_permitted(agreement.tenant)

        # User with 'House Owner' role and correct house should be permitted
        frappe.set_user("owner@example.com")
        agreement.tenant = "Test Tenant"
        agreement.house = "Test House"
        agreement.is_permitted(agreement.tenant)

        # User with 'House Owner' role and incorrect house should raise an exception
        frappe.set_user("owner@example.com")
        agreement.tenant = "Test Tenant"
        agreement.house = "Wrong House"
        with self.assertRaises(frappe.ValidationError):
            agreement.is_permitted(agreement.tenant)

    def test_set_end_date(self):
        agreement = RentalAgreement()
        agreement.start_date = "2023-01-01"

        # Monthly rent type should calculate end date correctly
        agreement.lease_term_count = 6
        agreement.house = "Test House"
        agreement.set_end_date()
        expected_end_date = convert_to_date_object("2023-07-01")
        self.assertEqual(agreement.end_date, expected_end_date)

        # Yearly rent type should calculate end date correctly
        agreement.lease_term_count = 3
        agreement.house = "Test House"
        agreement.set_end_date()
        expected_end_date = convert_to_date_object("2026-01-01")
        self.assertEqual(agreement.end_date, expected_end_date)
