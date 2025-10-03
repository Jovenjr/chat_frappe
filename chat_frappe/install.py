"""
Setup fixtures for Chat Frappe
"""

import frappe


def after_install():
	"""Install fixtures after app installation"""
	install_agents()


def install_agents():
	"""Install default agents"""
	import json
	import os
	
	# Get fixtures file path
	fixtures_path = os.path.join(
		frappe.get_app_path("chat_frappe"),
		"fixtures",
		"agent.json"
	)
	
	# Check if file exists
	if not os.path.exists(fixtures_path):
		return
	
	# Load fixtures
	with open(fixtures_path, "r", encoding="utf-8") as f:
		agents = json.load(f)
	
	# Install each agent
	for agent_data in agents:
		# Check if agent already exists
		if not frappe.db.exists("Agent", agent_data.get("agent_name")):
			agent = frappe.get_doc(agent_data)
			agent.insert(ignore_permissions=True)
			frappe.db.commit()
	
	print("Default agents installed successfully")
