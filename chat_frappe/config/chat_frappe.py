from frappe import _


def get_data():
	"""Return module information for Chat Frappe"""
	return [
		{
			"label": _("Chat"),
			"items": [
				{
					"type": "doctype",
					"name": "Agent",
					"label": _("Agent"),
					"description": _("Manage AI Agents")
				},
				{
					"type": "doctype",
					"name": "Chat Conversation",
					"label": _("Chat Conversation"),
					"description": _("View Chat Conversations")
				},
				{
					"type": "doctype",
					"name": "Chat Message",
					"label": _("Chat Message"),
					"description": _("View Chat Messages")
				},
				{
					"type": "page",
					"name": "chat",
					"label": _("Chat"),
					"description": _("Chat with AI Agents")
				}
			]
		}
	]
