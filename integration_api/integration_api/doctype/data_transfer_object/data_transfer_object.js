// Copyright (c) 2025, ahmedatef and contributors
// For license information, please see license.txt

frappe.ui.form.on("Data Transfer Object", {
    refresh(frm) {

    },
    integration_doctype(frm) {
        frm.call({
            doc: frm.doc,
            method: "update_integration_fields",

        }).then((r) => {
            if (r.message) {
                console.log(r.message);
                // console.log("done ");
                // if (!frm.doc.name) {
                //     frappe.throw("Please save the document first.");
                // }



                // frm.call({
                //     doc: frm.doc,
                //     method: "update_integration_fields",
                //     args: {
                //         data: r.message
                //     }
                // }).then((res) => {
                //     if (res.message) {
                //         console.log(res.message);
                //     }
                //     // console.log(res.message);
                // })

                // // frappe.msgprint("done calling");
            }

        })
    },

});