// Copyright (c) 2024, Chat Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Article', {
	// refresh: function(frm) {

	// },
	
	article_name: function(frm) {
		// Custom logic when article_name changes
		if (frm.doc.article_name) {
			frm.set_value('article_name', frm.doc.article_name.trim());
		}
	},

	author: function(frm) {
		// Custom logic when author changes
		if (frm.doc.author) {
			frm.set_value('author', frm.doc.author.trim());
		}
	},

	isbn: function(frm) {
		// Custom logic when ISBN changes
		if (frm.doc.isbn) {
			// Remove any non-alphanumeric characters except hyphens
			frm.set_value('isbn', frm.doc.isbn.replace(/[^a-zA-Z0-9-]/g, ''));
		}
	},

	status: function(frm) {
		// Custom logic when status changes
		if (frm.doc.status === 'Issued') {
			frm.set_value('status', 'Issued');
		} else {
			frm.set_value('status', 'Available');
		}
	},

	refresh: function(frm) {
		// Add custom buttons or modify the form
		if (frm.doc.status === 'Available') {
			frm.add_custom_button(__('Issue Article'), function() {
				frm.set_value('status', 'Issued');
				frm.save();
			}, __('Actions'));
		} else if (frm.doc.status === 'Issued') {
			frm.add_custom_button(__('Return Article'), function() {
				frm.set_value('status', 'Available');
				frm.save();
			}, __('Actions'));
		}
	}
});
