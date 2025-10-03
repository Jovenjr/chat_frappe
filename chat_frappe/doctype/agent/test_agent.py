# Copyright (c) 2024, Your Company and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestAgent(FrappeTestCase):
	def test_agent_creation(self):
		"""Test creating an agent"""
		agent = frappe.get_doc({
			"doctype": "Agent",
			"agent_name": "Test Agent",
			"agent_type": "General Assistant",
			"description": "Test agent for unit testing"
		})
		agent.insert()
		self.assertEqual(agent.agent_name, "Test Agent")
		agent.delete()
