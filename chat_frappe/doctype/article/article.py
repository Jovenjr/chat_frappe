# Copyright (c) 2024, Chat Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Article(Document):
	# this will auto-save on every change
	pass

	def before_save(self):
		# Add any custom logic before saving
		pass

	def after_save(self):
		# Add any custom logic after saving
		pass

	def validate(self):
		# Add any custom validation logic
		if self.isbn and len(self.isbn) < 10:
			frappe.throw("ISBN debe tener al menos 10 caracteres")

	def on_update(self):
		# Add any custom logic on update
		pass

	def on_cancel(self):
		# Add any custom logic on cancel
		pass

	def on_trash(self):
		# Add any custom logic on delete
		pass
