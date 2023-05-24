// Copyright (c) 2023, Akinola Marvellous and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tenant', {
    refresh: function (frm) {
        var filters = {};
        var owner = null;
        // console.log(user)
        if (frappe.user.has_role('House Owner') && !frappe.user.has_role('Administrator')) {
            getUser('House Owner')
                .then(function (user) {
                    owner = user
                    filters = {
                        'house_owner': owner.name,
                        'status': 'Available'
                    };
                    console.log('ow', owner.name);
                    frm.set_query('house', function () {
                        return {
                            filters: filters
                        };
                    });// Use the user object here
                })
                .catch(function (error) {
                    console.log('Error:', error);
                });

        } else {
            filters = {
                'status': 'Available'
            };
            frm.set_query('house', function () {
                return {
                    filters: filters
                };
            });
        }
        frm.add_custom_button('Create Agreement', () => {
            frappe.new_doc('Rental Agreement', {
                tenant: frm.doc.name,
                house: frm.doc.house,
                agent: frm.doc.agent,
            })
        })
    }
});


function getUser(doctype) {
    return new Promise(function (resolve, reject) {
        try {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: doctype,
                    filters: {
                        email: frappe.session.user_email
                    }
                },
                callback: function (response) {
                    var user = response.message;
                    resolve(user); // Resolve the Promise with the user object
                },
                error: function (xhr, textStatus, error) {
                    console.log('Error:', error);
                    // reject(error); // Reject the Promise with the error
                }
            });
        } catch (e) {
            console.log(e);
            reject(e); // Reject the Promise with the exception
        }
    });
}
