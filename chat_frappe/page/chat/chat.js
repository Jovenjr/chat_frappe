frappe.pages['chat'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Chat con Agentes',
		single_column: true
	});

	// Create chat interface
	page.chat = new ChatInterface(page);
}

class ChatInterface {
	constructor(page) {
		this.page = page;
		this.current_conversation = null;
		this.conversations = [];
		this.agents = [];
		
		this.make();
		this.load_data();
	}

	make() {
		// Create main layout
		this.page.$body.html(`
			<div class="chat-container">
				<div class="chat-sidebar">
					<div class="chat-sidebar-header">
						<h4>Mis Agentes</h4>
					</div>
					<div class="chat-contacts-list" id="chat-contacts-list">
						<div class="text-center text-muted" style="padding: 20px;">
							Cargando...
						</div>
					</div>
				</div>
				<div class="chat-main">
					<div class="chat-empty-state" id="chat-empty-state">
						<div class="text-center text-muted">
							<i class="fa fa-comments fa-4x" style="opacity: 0.3;"></i>
							<p style="margin-top: 20px;">Selecciona un agente para comenzar a chatear</p>
						</div>
					</div>
					<div class="chat-conversation-view" id="chat-conversation-view" style="display: none;">
						<div class="chat-header" id="chat-header">
							<div class="chat-header-info">
								<img class="chat-avatar" src="/assets/frappe/images/default-avatar.png" id="chat-agent-avatar">
								<div class="chat-header-text">
									<h5 id="chat-agent-name">Agent Name</h5>
									<small id="chat-agent-status" class="text-muted">Online</small>
								</div>
							</div>
						</div>
						<div class="chat-messages" id="chat-messages">
							<!-- Messages will be loaded here -->
						</div>
						<div class="chat-input-area">
							<div class="chat-input-wrapper">
								<textarea 
									class="form-control chat-input" 
									id="chat-message-input" 
									placeholder="Escribe un mensaje..."
									rows="1"
								></textarea>
								<button class="btn btn-primary btn-send" id="btn-send-message">
									<i class="fa fa-paper-plane"></i>
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		`);

		this.setup_styles();
		this.setup_events();
	}

	setup_styles() {
		const style = `
			<style>
				.chat-container {
					display: flex;
					height: calc(100vh - 120px);
					background: white;
					border-radius: 8px;
					overflow: hidden;
					box-shadow: 0 1px 3px rgba(0,0,0,0.1);
				}
				
				.chat-sidebar {
					width: 350px;
					border-right: 1px solid #e0e0e0;
					display: flex;
					flex-direction: column;
				}
				
				.chat-sidebar-header {
					padding: 20px;
					border-bottom: 1px solid #e0e0e0;
					background: #f8f9fa;
				}
				
				.chat-sidebar-header h4 {
					margin: 0;
					font-size: 18px;
					color: #333;
				}
				
				.chat-contacts-list {
					flex: 1;
					overflow-y: auto;
				}
				
				.chat-contact-item {
					display: flex;
					align-items: center;
					padding: 15px 20px;
					cursor: pointer;
					border-bottom: 1px solid #f0f0f0;
					transition: background 0.2s;
				}
				
				.chat-contact-item:hover {
					background: #f5f5f5;
				}
				
				.chat-contact-item.active {
					background: #e3f2fd;
				}
				
				.chat-avatar {
					width: 50px;
					height: 50px;
					border-radius: 50%;
					margin-right: 15px;
					object-fit: cover;
				}
				
				.chat-contact-info {
					flex: 1;
					min-width: 0;
				}
				
				.chat-contact-name {
					font-weight: 600;
					color: #333;
					margin-bottom: 3px;
				}
				
				.chat-contact-status {
					font-size: 12px;
					color: #666;
				}
				
				.chat-unread-badge {
					background: #00A8E8;
					color: white;
					border-radius: 12px;
					padding: 2px 8px;
					font-size: 11px;
					font-weight: 600;
				}
				
				.chat-main {
					flex: 1;
					display: flex;
					flex-direction: column;
					position: relative;
				}
				
				.chat-empty-state {
					display: flex;
					align-items: center;
					justify-content: center;
					height: 100%;
				}
				
				.chat-conversation-view {
					display: flex;
					flex-direction: column;
					height: 100%;
				}
				
				.chat-header {
					padding: 15px 20px;
					border-bottom: 1px solid #e0e0e0;
					background: #f8f9fa;
				}
				
				.chat-header-info {
					display: flex;
					align-items: center;
				}
				
				.chat-header-text h5 {
					margin: 0;
					font-size: 16px;
					color: #333;
				}
				
				.chat-messages {
					flex: 1;
					overflow-y: auto;
					padding: 20px;
					background: #f5f5f5;
				}
				
				.chat-message {
					display: flex;
					margin-bottom: 15px;
					animation: messageSlide 0.3s ease-out;
				}
				
				@keyframes messageSlide {
					from {
						opacity: 0;
						transform: translateY(10px);
					}
					to {
						opacity: 1;
						transform: translateY(0);
					}
				}
				
				.chat-message.sent {
					justify-content: flex-end;
				}
				
				.chat-message-bubble {
					max-width: 70%;
					padding: 10px 15px;
					border-radius: 12px;
					word-wrap: break-word;
				}
				
				.chat-message.received .chat-message-bubble {
					background: white;
					border: 1px solid #e0e0e0;
					border-bottom-left-radius: 4px;
				}
				
				.chat-message.sent .chat-message-bubble {
					background: #00A8E8;
					color: white;
					border-bottom-right-radius: 4px;
				}
				
				.chat-message-time {
					font-size: 11px;
					margin-top: 5px;
					opacity: 0.7;
				}
				
				.chat-input-area {
					padding: 15px 20px;
					border-top: 1px solid #e0e0e0;
					background: white;
				}
				
				.chat-input-wrapper {
					display: flex;
					gap: 10px;
					align-items: flex-end;
				}
				
				.chat-input {
					flex: 1;
					resize: none;
					border: 1px solid #d0d0d0;
					border-radius: 8px;
					padding: 10px;
					max-height: 120px;
				}
				
				.btn-send {
					height: 40px;
					width: 40px;
					border-radius: 50%;
					padding: 0;
					display: flex;
					align-items: center;
					justify-content: center;
				}
				
				.chat-typing-indicator {
					display: flex;
					gap: 4px;
					padding: 10px 15px;
				}
				
				.chat-typing-dot {
					width: 8px;
					height: 8px;
					border-radius: 50%;
					background: #999;
					animation: typing 1.4s infinite;
				}
				
				.chat-typing-dot:nth-child(2) {
					animation-delay: 0.2s;
				}
				
				.chat-typing-dot:nth-child(3) {
					animation-delay: 0.4s;
				}
				
				@keyframes typing {
					0%, 60%, 100% {
						transform: translateY(0);
					}
					30% {
						transform: translateY(-10px);
					}
				}
				
				.status-online {
					color: #4caf50;
				}
				
				.status-busy {
					color: #ff9800;
				}
				
				.status-offline {
					color: #9e9e9e;
				}
			</style>
		`;
		this.page.$body.prepend(style);
	}

	setup_events() {
		const me = this;

		// Send message on button click
		this.page.$body.find('#btn-send-message').on('click', function() {
			me.send_message();
		});

		// Send message on Enter (Shift+Enter for new line)
		this.page.$body.find('#chat-message-input').on('keydown', function(e) {
			if (e.key === 'Enter' && !e.shiftKey) {
				e.preventDefault();
				me.send_message();
			}
		});

		// Auto-resize textarea
		this.page.$body.find('#chat-message-input').on('input', function() {
			this.style.height = 'auto';
			this.style.height = Math.min(this.scrollHeight, 120) + 'px';
		});
	}

	async load_data() {
		try {
			// Load agents
			const agents_response = await frappe.call({
				method: 'chat_frappe.chat_frappe.api.get_agents'
			});
			this.agents = agents_response.message || [];

			// Load conversations
			const conv_response = await frappe.call({
				method: 'chat_frappe.chat_frappe.api.get_conversations'
			});
			this.conversations = conv_response.message || [];

			this.render_contacts();
		} catch (error) {
			console.error('Error loading data:', error);
			frappe.msgprint('Error al cargar los datos del chat');
		}
	}

	render_contacts() {
		const $list = this.page.$body.find('#chat-contacts-list');
		$list.empty();

		if (this.agents.length === 0) {
			$list.html(`
				<div class="text-center text-muted" style="padding: 20px;">
					No hay agentes disponibles.<br>
					<a href="/app/agent">Crear un agente</a>
				</div>
			`);
			return;
		}

		// Render each agent as a contact
		this.agents.forEach(agent => {
			// Find conversation for this agent
			const conversation = this.conversations.find(c => c.agent === agent.name);
			
			const $contact = $(`
				<div class="chat-contact-item" data-agent="${agent.name}">
					<img class="chat-avatar" src="${agent.avatar || '/assets/frappe/images/default-avatar.png'}" alt="${agent.agent_name}">
					<div class="chat-contact-info">
						<div class="chat-contact-name">${agent.agent_name}</div>
						<div class="chat-contact-status status-${agent.status.toLowerCase()}">${agent.description || agent.agent_type}</div>
					</div>
					${conversation && conversation.unread_count > 0 ? `<span class="chat-unread-badge">${conversation.unread_count}</span>` : ''}
				</div>
			`);

			$contact.on('click', () => {
				this.open_conversation(agent);
			});

			$list.append($contact);
		});
	}

	async open_conversation(agent) {
		try {
			// Get or create conversation
			const response = await frappe.call({
				method: 'chat_frappe.chat_frappe.api.get_or_create_conversation',
				args: { agent: agent.name }
			});
			
			this.current_conversation = response.message;
			this.current_agent = agent;

			// Update UI
			this.page.$body.find('.chat-contact-item').removeClass('active');
			this.page.$body.find(`.chat-contact-item[data-agent="${agent.name}"]`).addClass('active');

			this.page.$body.find('#chat-empty-state').hide();
			this.page.$body.find('#chat-conversation-view').show();

			// Update header
			this.page.$body.find('#chat-agent-avatar').attr('src', agent.avatar || '/assets/frappe/images/default-avatar.png');
			this.page.$body.find('#chat-agent-name').text(agent.agent_name);
			this.page.$body.find('#chat-agent-status').text(agent.status).attr('class', `text-muted status-${agent.status.toLowerCase()}`);

			// Load messages
			await this.load_messages();
		} catch (error) {
			console.error('Error opening conversation:', error);
			frappe.msgprint('Error al abrir la conversación');
		}
	}

	async load_messages() {
		try {
			const response = await frappe.call({
				method: 'chat_frappe.chat_frappe.api.get_messages',
				args: { conversation: this.current_conversation.name }
			});

			const messages = response.message || [];
			this.render_messages(messages);
		} catch (error) {
			console.error('Error loading messages:', error);
		}
	}

	render_messages(messages) {
		const $container = this.page.$body.find('#chat-messages');
		$container.empty();

		messages.forEach(msg => {
			const is_sent = msg.sender_type === 'User';
			const time = moment(msg.timestamp).format('HH:mm');

			const $message = $(`
				<div class="chat-message ${is_sent ? 'sent' : 'received'}">
					<div class="chat-message-bubble">
						<div class="chat-message-text">${frappe.utils.escape_html(msg.message)}</div>
						<div class="chat-message-time">${time}</div>
					</div>
				</div>
			`);

			$container.append($message);
		});

		// Scroll to bottom
		$container.scrollTop($container[0].scrollHeight);
	}

	async send_message() {
		const $input = this.page.$body.find('#chat-message-input');
		const message = $input.val().trim();

		if (!message || !this.current_conversation) {
			return;
		}

		// Clear input
		$input.val('');
		$input.css('height', 'auto');

		// Add user message to UI immediately
		this.add_message_to_ui('User', message);

		// Show typing indicator
		this.show_typing_indicator();

		try {
			const response = await frappe.call({
				method: 'chat_frappe.chat_frappe.api.send_message',
				args: {
					conversation: this.current_conversation.name,
					message: message
				}
			});

			// Remove typing indicator
			this.hide_typing_indicator();

			if (response.message.success) {
				// Add agent response to UI
				const agent_msg = response.message.agent_message;
				this.add_message_to_ui('Agent', agent_msg.message);
			} else {
				frappe.msgprint('Error al enviar el mensaje');
			}
		} catch (error) {
			this.hide_typing_indicator();
			console.error('Error sending message:', error);
			frappe.msgprint('Error al enviar el mensaje');
		}
	}

	add_message_to_ui(sender_type, message) {
		const $container = this.page.$body.find('#chat-messages');
		const is_sent = sender_type === 'User';
		const time = moment().format('HH:mm');

		const $message = $(`
			<div class="chat-message ${is_sent ? 'sent' : 'received'}">
				<div class="chat-message-bubble">
					<div class="chat-message-text">${frappe.utils.escape_html(message)}</div>
					<div class="chat-message-time">${time}</div>
				</div>
			</div>
		`);

		$container.append($message);
		$container.scrollTop($container[0].scrollHeight);
	}

	show_typing_indicator() {
		const $container = this.page.$body.find('#chat-messages');
		const $indicator = $(`
			<div class="chat-message received" id="typing-indicator">
				<div class="chat-message-bubble">
					<div class="chat-typing-indicator">
						<div class="chat-typing-dot"></div>
						<div class="chat-typing-dot"></div>
						<div class="chat-typing-dot"></div>
					</div>
				</div>
			</div>
		`);
		$container.append($indicator);
		$container.scrollTop($container[0].scrollHeight);
	}

	hide_typing_indicator() {
		this.page.$body.find('#typing-indicator').remove();
	}
}
