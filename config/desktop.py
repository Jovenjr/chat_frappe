from frappe import _


def get_data():
	return [
		{
			"module_name": "Chat Frappe",
			"category": "Modules",
			"color": "#00A8E8",
			"icon": "octicon octicon-comment-discussion",
			"type": "module",
			"label": _("Chat"),
			"description": _("Sistema de chat con agentes IA"),
			"onboard_present": 0
		}
	]
