// Copyright (c) 2023, Akinola Marvellous and contributors
// For license information, please see license.txt

frappe.ui.form.on("House", {
    refresh(frm) {
        if (frm.doc.status === "Available") {
            frm.add_custom_button('Add new Tenant', () => {
                frappe.new_doc('Tenant', {
                    house: frm.doc.name,
                })
            })
        }
    },
});
