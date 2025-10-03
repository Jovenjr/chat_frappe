# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Agent(Document):
	def validate(self):
		"""Validate agent configuration"""
		if not self.system_prompt:
			self.system_prompt = f"You are {self.agent_name}, a helpful {self.agent_type} assistant."
	
	def get_api_config(self):
		"""Get API configuration for this agent"""
		return {
			"endpoint": self.api_endpoint or frappe.conf.get("chat_agent_api_url"),
			"api_key": self.get_password("api_key") or frappe.conf.get("chat_agent_api_key"),
			"model": self.model_name,
			"temperature": self.temperature,
			"max_tokens": self.max_tokens,
			"system_prompt": self.system_prompt
		}
