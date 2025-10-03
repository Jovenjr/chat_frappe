# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ChatMessage(Document):
	def after_insert(self):
		"""Update conversation after inserting a new message"""
		conversation = frappe.get_doc("Chat Conversation", self.conversation)
		conversation.last_message_time = self.timestamp
		
		# Increment unread count if message is from agent
		if self.sender_type == "Agent":
			conversation.unread_count = (conversation.unread_count or 0) + 1
		
		conversation.save(ignore_permissions=True)
