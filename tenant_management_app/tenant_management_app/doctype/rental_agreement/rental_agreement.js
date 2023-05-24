// Copyright (c) 2023, Akinola Marvellous and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rental Agreement", {
	refresh(frm) {
        frm.add_custom_button('Create Billing', () => {
            frappe.new_doc('Billing', {
                agreement: frm.doc.name,
                tenant: frm.doc.tenant,
                house: frm.doc.house,
                rent_amount: frm.doc.rent_amount,
            })
        })
        console.log('Create Billing,', frm.doc.name, frm.doc.rent_amount)
	},
});
