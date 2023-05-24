// Copyright (c) 2023, Akinola Marvellous and contributors
// For license information, please see license.txt

frappe.ui.form.on("Billing", {
    refresh(frm) {
        let is_allowed = frappe.user_roles.includes('House Agent');
        frm.toggle_enable('agency_fee', is_allowed);
    },
});
// frappe.ui.form.on('MyDoc', {
//     refresh: function(frm) {
//         var isAgent = frappe.user.has_role('Agent');
//         frm.toggle_display('field_name', isAgent);
//     }
// });

