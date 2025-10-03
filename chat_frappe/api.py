# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import json


@frappe.whitelist()
def get_conversations():
	"""Get all conversations for the current user"""
	user = frappe.session.user
	
	conversations = frappe.get_all(
		"Chat Conversation",
		filters={
			"user": user,
			"status": "Active"
		},
		fields=["name", "agent", "conversation_title", "last_message_time", "unread_count"],
		order_by="last_message_time desc"
	)
	
	# Get agent details for each conversation
	for conv in conversations:
		agent = frappe.get_doc("Agent", conv.agent)
		conv.agent_details = {
			"name": agent.agent_name,
			"avatar": agent.avatar,
			"status": agent.status,
			"description": agent.description
		}
	
	return conversations


@frappe.whitelist()
def get_or_create_conversation(agent):
	"""Get existing conversation or create a new one with an agent"""
	user = frappe.session.user
	
	# Check if conversation already exists
	existing = frappe.db.exists("Chat Conversation", {
		"user": user,
		"agent": agent,
		"status": "Active"
	})
	
	if existing:
		return frappe.get_doc("Chat Conversation", existing)
	
	# Create new conversation
	conversation = frappe.get_doc({
		"doctype": "Chat Conversation",
		"user": user,
		"agent": agent
	})
	conversation.insert(ignore_permissions=True)
	
	return conversation


@frappe.whitelist()
def get_messages(conversation, limit=50):
	"""Get messages for a conversation"""
	# Verify user has access to this conversation
	conv = frappe.get_doc("Chat Conversation", conversation)
	if conv.user != frappe.session.user:
		frappe.throw(_("Not authorized"), frappe.PermissionError)
	
	messages = frappe.get_all(
		"Chat Message",
		filters={"conversation": conversation},
		fields=["name", "sender_type", "sender", "message", "timestamp", "message_type", "is_read"],
		order_by="timestamp asc",
		limit=limit
	)
	
	# Mark conversation as read
	conv.mark_as_read()
	
	return messages


@frappe.whitelist()
def send_message(conversation, message, message_type="Text"):
	"""Send a message and get agent response"""
	from chat_frappe.agent_service import AgentService
	
	# Verify user has access to this conversation
	conv = frappe.get_doc("Chat Conversation", conversation)
	if conv.user != frappe.session.user:
		frappe.throw(_("Not authorized"), frappe.PermissionError)
	
	# Save user message
	user_message = frappe.get_doc({
		"doctype": "Chat Message",
		"conversation": conversation,
		"sender_type": "User",
		"sender": frappe.session.user,
		"message": message,
		"message_type": message_type,
		"is_read": True
	})
	user_message.insert(ignore_permissions=True)
	
	# Get agent response
	try:
		agent_service = AgentService(conv.agent)
		response = agent_service.get_response(message, conversation)
		
		# Save agent response
		agent_message = frappe.get_doc({
			"doctype": "Chat Message",
			"conversation": conversation,
			"sender_type": "Agent",
			"sender": conv.agent,
			"message": response,
			"message_type": "Text",
			"is_read": False
		})
		agent_message.insert(ignore_permissions=True)
		
		return {
			"success": True,
			"user_message": user_message.as_dict(),
			"agent_message": agent_message.as_dict()
		}
	
	except Exception as e:
		frappe.log_error(f"Error getting agent response: {str(e)}")
		
		# Save error message
		error_message = frappe.get_doc({
			"doctype": "Chat Message",
			"conversation": conversation,
			"sender_type": "Agent",
			"sender": conv.agent,
			"message": _("Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta de nuevo."),
			"message_type": "System",
			"is_read": False
		})
		error_message.insert(ignore_permissions=True)
		
		return {
			"success": False,
			"error": str(e),
			"user_message": user_message.as_dict(),
			"agent_message": error_message.as_dict()
		}


@frappe.whitelist()
def get_agents():
	"""Get all active agents"""
	agents = frappe.get_all(
		"Agent",
		filters={"is_active": 1},
		fields=["name", "agent_name", "agent_type", "description", "avatar", "status"]
	)
	
	return agents


@frappe.whitelist()
def mark_conversation_read(conversation):
	"""Mark all messages in a conversation as read"""
	conv = frappe.get_doc("Chat Conversation", conversation)
	if conv.user != frappe.session.user:
		frappe.throw(_("Not authorized"), frappe.PermissionError)
	
	conv.mark_as_read()
	
	return {"success": True}
