"""
Setup fixtures for Chat Frappe
"""

import frappe


def after_install():
	"""Install fixtures after app installation"""
	print("Chat Frappe installed successfully!")
	print("Please run: bench --site [site-name] migrate to create the database tables")
	print("Then use Frappe UI to create your agents manually or import the fixtures")
