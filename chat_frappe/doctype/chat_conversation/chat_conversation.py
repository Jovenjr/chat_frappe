# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ChatConversation(Document):
	def before_save(self):
		"""Update conversation title if not set"""
		if not self.conversation_title:
			agent = frappe.get_doc("Agent", self.agent)
			self.conversation_title = f"Chat with {agent.agent_name}"
	
	def mark_as_read(self):
		"""Mark all messages in this conversation as read"""
		self.unread_count = 0
		self.save(ignore_permissions=True)
