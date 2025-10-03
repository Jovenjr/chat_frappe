# Estructura de la Aplicación Chat Frappe

Esta aplicación sigue la estructura estándar de Frappe Framework.

## Estructura de Directorios

```
chat_frappe/                    # Raíz de la app
│
├── __init__.py                 # Versión de la app
├── hooks.py                    # Configuración principal y hooks de la app
├── pyproject.toml              # Configuración de Python y dependencias
├── LICENSE                     # Licencia MIT
├── README.md                   # Documentación principal
├── INSTALL.md                  # Guía de instalación
├── API_CONFIG.md               # Configuración de APIs
│
├── config/                     # Configuraciones de módulos y escritorio
│   ├── __init__.py
│   ├── desktop.py              # Configuración del módulo en el escritorio
│   └── docs.py                 # Configuración de documentación
│
└── chat_frappe/                # Módulo principal de la aplicación
    │
    ├── __init__.py             # Inicialización del módulo
    ├── api.py                  # Endpoints API REST
    ├── agent_service.py        # Servicio de integración con agentes
    ├── install.py              # Scripts de instalación
    │
    ├── config/                 # Configuración del módulo
    │   ├── __init__.py
    │   └── chat_frappe.py      # Items del módulo (DocTypes, Pages, etc.)
    │
    ├── doctype/                # DocTypes de la aplicación
    │   ├── __init__.py
    │   │
    │   ├── agent/              # DocType: Agent
    │   │   ├── __init__.py
    │   │   ├── agent.json      # Definición del DocType
    │   │   ├── agent.py        # Controlador Python
    │   │   └── test_agent.py   # Tests unitarios
    │   │
    │   ├── chat_conversation/  # DocType: Chat Conversation
    │   │   ├── __init__.py
    │   │   ├── chat_conversation.json
    │   │   ├── chat_conversation.py
    │   │   └── test_chat_conversation.py
    │   │
    │   └── chat_message/       # DocType: Chat Message
    │       ├── __init__.py
    │       ├── chat_message.json
    │       ├── chat_message.py
    │       └── test_chat_message.py
    │
    ├── page/                   # Páginas personalizadas
    │   ├── __init__.py
    │   │
    │   └── chat/               # Página: Chat
    │       ├── __init__.py
    │       ├── chat.json       # Definición de la página
    │       └── chat.js         # JavaScript de la página
    │
    ├── fixtures/               # Datos iniciales (fixtures)
    │   └── agent.json          # Agentes predefinidos
    │
    └── public/                 # Archivos estáticos públicos
        ├── css/
        │   └── chat_frappe.css # Estilos globales
        └── js/
            └── chat_frappe.js  # JavaScript global
```

## Componentes Principales

### DocTypes

**Agent** - Gestión de agentes de IA
- Configuración de API
- Personalización de comportamiento
- Avatares y estados

**Chat Conversation** - Conversaciones entre usuarios y agentes
- Gestión de sesiones de chat
- Contador de mensajes no leídos
- Historial de conversaciones

**Chat Message** - Mensajes individuales
- Almacenamiento de mensajes
- Tipos de mensaje (texto, imagen, archivo, etc.)
- Timestamps y estado de lectura

### Pages

**Chat** - Interfaz principal de chat
- Diseño estilo WhatsApp
- Lista de contactos (agentes)
- Ventana de conversación
- Input de mensajes

### API Endpoints

Todos en `chat_frappe/api.py`:
- `get_conversations()` - Lista de conversaciones del usuario
- `get_or_create_conversation()` - Obtener/crear conversación
- `get_messages()` - Mensajes de una conversación
- `send_message()` - Enviar mensaje y recibir respuesta
- `get_agents()` - Lista de agentes activos
- `mark_conversation_read()` - Marcar como leído

### Servicios

**AgentService** (`agent_service.py`)
- Integración con APIs externas de IA
- Gestión de historial de conversaciones
- Manejo de diferentes formatos de API

## Convenciones de Frappe

✅ **Estructura correcta según Frappe Framework:**
- App en raíz: `chat_frappe/`
- Módulo principal: `chat_frappe/chat_frappe/`
- DocTypes en: `chat_frappe/chat_frappe/doctype/`
- Páginas en: `chat_frappe/chat_frappe/page/`
- Config en: `chat_frappe/config/` (raíz) y `chat_frappe/chat_frappe/config/` (módulo)

✅ **Archivos requeridos:**
- `__init__.py` con `__version__`
- `hooks.py` con configuración de la app
- `pyproject.toml` con metadatos

✅ **Naming conventions:**
- DocTypes: PascalCase con espacios (`Chat Conversation`)
- Archivos Python: snake_case
- Nombres de apps: snake_case

## Referencias

- [Frappe Framework Docs](https://frappeframework.com/docs)
- [App Structure](https://frappeframework.com/docs/user/en/basics/doctypes)
- [Hooks Reference](https://frappeframework.com/docs/user/en/python-api/hooks)
