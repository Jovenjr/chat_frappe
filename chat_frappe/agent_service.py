# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
import requests
import json
from frappe import _


class AgentService:
	"""Service to communicate with AI agents"""
	
	def __init__(self, agent_name):
		self.agent = frappe.get_doc("Agent", agent_name)
		self.config = self.agent.get_api_config()
		# Mapeo de nombres de agentes a tipos de agentes en la API
		self.agent_type_map = {
			"Ingeniero TI": "ingeniero_ti",
			"Ingeniero Nube": "ingeniero_nube", 
			"Asesor Legal": "asesor_legal",
		}
	
	def get_response(self, message, conversation_id=None):
		"""Get response from the agent"""
		
		# Get session_id from conversation metadata
		session_id = None
		if conversation_id:
			session_id = self._get_or_create_session(conversation_id)
		
		# Prepare the request
		payload = self._prepare_payload(message, session_id)
		
		# Call the agent API
		response = self._call_agent_api(payload)
		
		return response
	
	def _get_or_create_session(self, conversation_id):
		"""Get or create session ID for the conversation"""
		
		# Get conversation to check for existing session_id
		conv = frappe.get_doc("Chat Conversation", conversation_id)
		
		# Check if we have stored a session_id in metadata
		metadata = {}
		if hasattr(conv, 'metadata') and conv.metadata:
			try:
				metadata = json.loads(conv.metadata) if isinstance(conv.metadata, str) else conv.metadata
			except:
				metadata = {}
		
		if metadata.get('session_id'):
			return metadata['session_id']
		
		# Create new session via API
		try:
			agent_type = self._get_agent_type()
			endpoint = self.config.get("endpoint")
			if not endpoint:
				frappe.throw(_("API endpoint not configured for this agent"))
			
			# Remove trailing slash and add /sessions/new
			base_url = endpoint.rstrip('/')
			if '/query' in base_url or '/chat' in base_url:
				base_url = base_url.rsplit('/', 1)[0]
			
			session_url = f"{base_url}/sessions/new"
			
			headers = self._get_headers()
			
			session_payload = {
				"agent_type": agent_type,
				"metadata": {
					"conversation_id": conversation_id,
					"agent_name": self.agent.agent_name
				}
			}
			
			response = requests.post(
				session_url,
				json=session_payload,
				headers=headers,
				timeout=10
			)
			
			response.raise_for_status()
			result = response.json()
			
			session_id = result.get('session_id')
			
			# Store session_id in conversation metadata
			if session_id:
				metadata['session_id'] = session_id
				conv.db_set('metadata', json.dumps(metadata), update_modified=False)
			
			return session_id
			
		except Exception as e:
			frappe.log_error(f"Error creating session: {str(e)}", "Agent Service")
			return None
	
	def _get_agent_type(self):
		"""Get the agent type for the API"""
		agent_name = self.agent.agent_name
		
		# Check if agent has custom metadata with agent_type
		if hasattr(self.agent, 'metadata') and self.agent.metadata:
			try:
				metadata = json.loads(self.agent.metadata) if isinstance(self.agent.metadata, str) else self.agent.metadata
				if metadata.get('agent_type'):
					return metadata['agent_type']
			except:
				pass
		
		# Use mapping or default
		return self.agent_type_map.get(agent_name, "ingeniero_ti")
	
	def _prepare_payload(self, message, session_id=None):
		"""Prepare the API payload for the multi-agent API"""
		
		agent_type = self._get_agent_type()
		
		# Build payload according to QueryRequest schema
		payload = {
			"agent_type": agent_type,
			"query": message
		}
		
		# Add session_id if available
		if session_id:
			payload["session_id"] = session_id
		
		# Add context if system prompt exists
		if self.config.get("system_prompt"):
			payload["context"] = {
				"system_prompt": self.config["system_prompt"],
				"temperature": self.config.get("temperature", 0.7),
				"max_tokens": self.config.get("max_tokens", 2000)
			}
		
		return payload
	
	def _get_headers(self):
		"""Get headers for API requests"""
		headers = {
			"Content-Type": "application/json"
		}
		
		api_key = self.config.get("api_key")
		if api_key:
			headers["Authorization"] = f"Bearer {api_key}"
		
		return headers
	
	def _call_agent_api(self, payload):
		"""Call the external agent API"""
		
		endpoint = self.config.get("endpoint")
		if not endpoint:
			frappe.throw(_("API endpoint not configured for this agent"))
		
		# Use /chat endpoint (or /query as fallback)
		if not endpoint.endswith('/chat') and not endpoint.endswith('/query'):
			endpoint = endpoint.rstrip('/') + '/chat'
		
		headers = self._get_headers()
		
		try:
			# Make the API call to the multi-agent API
			response = requests.post(
				endpoint,
				json=payload,
				headers=headers,
				timeout=30
			)
			
			response.raise_for_status()
			
			# Parse response according to QueryResponse schema
			result = response.json()
			
			# Extract response from QueryResponse
			if "response" in result:
				response_text = result["response"]
				
				# Log token usage if available
				if "token_usage" in result:
					token_usage = result["token_usage"]
					frappe.logger().info(f"Token usage - Prompt: {token_usage.get('prompt_tokens', 0)}, "
					                    f"Completion: {token_usage.get('completion_tokens', 0)}, "
					                    f"Total: {token_usage.get('total_tokens', 0)}")
				
				# Log sources if RAG was used
				if "sources" in result and result["sources"]:
					frappe.logger().info(f"RAG sources used: {len(result['sources'])}")
				
				return response_text
			else:
				# Fallback: return the whole result as JSON string
				return json.dumps(result, indent=2)
		
		except requests.exceptions.HTTPError as e:
			error_detail = ""
			try:
				error_data = e.response.json()
				error_detail = error_data.get("detail", str(error_data))
			except:
				error_detail = str(e)
			
			frappe.log_error(f"Agent API HTTP Error: {error_detail}", "Agent Service")
			frappe.throw(_("Error from agent API: {0}").format(error_detail))
		
		except requests.exceptions.RequestException as e:
			frappe.log_error(f"Agent API Connection Error: {str(e)}", "Agent Service")
			frappe.throw(_("Error connecting to agent: {0}").format(str(e)))
		
		except Exception as e:
			frappe.log_error(f"Agent Processing Error: {str(e)}", "Agent Service")
			frappe.throw(_("Error processing agent response: {0}").format(str(e)))
