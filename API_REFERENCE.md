# API Reference - Sistema Multi-Agente

Documentación completa de la integración entre Chat Frappe y tu API Multi-Agente.

## Arquitectura de Integración

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Chat Frappe   │────────▶│  Agent Service   │────────▶│  Multi-Agent    │
│   (Frontend)    │         │  (Middleware)    │         │     API         │
└─────────────────┘         └──────────────────┘         └─────────────────┘
     │                              │                            │
     │                              │                            │
     ▼                              ▼                            ▼
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│  Chat Message   │         │  Session Mgmt    │         │  RAG Engine     │
│   (DocType)     │         │  (Metadata)      │         │  (Docs + LLM)   │
└─────────────────┘         └──────────────────┘         └─────────────────┘
```

## Endpoints Utilizados

### 1. POST /chat - Enviar Mensaje

**Uso**: Endpoint principal para conversaciones con agentes

**Request**:
```json
{
  "agent_type": "ingeniero_ti",
  "query": "¿Cómo configuro SSH en Ubuntu?",
  "session_id": "abc-123-def-456",
  "context": {
    "system_prompt": "Eres un experto...",
    "temperature": 0.7,
    "max_tokens": 2000
  }
}
```

**Response**:
```json
{
  "agent_type": "ingeniero_ti",
  "response": "Para configurar SSH en Ubuntu:\n1. Instala openssh-server...",
  "session_id": "abc-123-def-456",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "token_usage": {
    "prompt_tokens": 120,
    "completion_tokens": 280,
    "total_tokens": 400
  },
  "sources": [
    {
      "title": "Ubuntu SSH Guide",
      "relevance": 0.92,
      "content": "...",
      "metadata": {}
    }
  ]
}
```

**Códigos de Estado**:
- `200` - Éxito
- `422` - Error de validación (agent_type inválido, query vacío, etc.)
- `500` - Error interno del servidor

---

### 2. POST /sessions/new - Crear Sesión

**Uso**: Crear una nueva sesión de conversación para mantener contexto

**Request**:
```json
{
  "agent_type": "ingeniero_nube",
  "metadata": {
    "conversation_id": "CHAT-0001",
    "agent_name": "Ingeniero Nube",
    "user_id": "user@example.com"
  }
}
```

**Response**:
```json
{
  "session_id": "xyz-789-abc-012",
  "agent_type": "ingeniero_nube",
  "created_at": "2024-01-01T12:00:00.000Z"
}
```

**Notas**:
- El `session_id` se guarda automáticamente en `Chat Conversation.metadata`
- Las sesiones permiten mantener contexto entre múltiples mensajes
- Una sesión = Una conversación completa con un agente

---

### 3. GET /sessions/{session_id}/history - Obtener Historial

**Uso**: Recuperar el historial completo de una sesión

**Request**:
```
GET /sessions/abc-123-def-456/history
```

**Response**:
```json
{
  "session_id": "abc-123-def-456",
  "agent_type": "asesor_legal",
  "messages": [
    {
      "role": "user",
      "content": "¿Qué cláusulas debe tener un SLA?",
      "timestamp": "2024-01-01T12:00:00.000Z"
    },
    {
      "role": "assistant",
      "content": "Un SLA debe incluir...",
      "timestamp": "2024-01-01T12:00:05.000Z"
    }
  ],
  "created_at": "2024-01-01T12:00:00.000Z",
  "updated_at": "2024-01-01T12:10:00.000Z",
  "metadata": {
    "total_messages": 10,
    "conversation_id": "CHAT-0001"
  }
}
```

---

### 4. GET /agents - Listar Agentes

**Uso**: Obtener información de todos los agentes disponibles

**Request**:
```
GET /agents
```

**Response**:
```json
{
  "ingeniero_ti": {
    "name": "Carlos Mendoza",
    "description": "Ingeniero TI especializado en infraestructura, redes y servidores",
    "status": "ready",
    "capabilities": ["linux", "networking", "security", "databases"],
    "rag_enabled": true
  },
  "ingeniero_nube": {
    "name": "Ana García",
    "description": "Ingeniera de nube experta en AWS, Azure, GCP",
    "status": "ready",
    "capabilities": ["aws", "azure", "gcp", "kubernetes", "terraform"],
    "rag_enabled": true
  },
  "asesor_legal": {
    "name": "María López",
    "description": "Asesora legal especializada en tecnología",
    "status": "ready",
    "capabilities": ["contracts", "gdpr", "compliance", "ip"],
    "rag_enabled": true
  }
}
```

---

### 5. GET /agents/{agent_type}/status - Estado del Agente

**Uso**: Verificar el estado operacional de un agente específico

**Request**:
```
GET /agents/ingeniero_ti/status
```

**Response**:
```json
{
  "agent_type": "ingeniero_ti",
  "name": "Carlos Mendoza",
  "status": "ready",
  "total_queries": 1523,
  "uptime_seconds": 86400.5,
  "last_query_at": "2024-01-01T12:00:00.000Z",
  "error_message": null
}
```

**Estados Posibles**:
- `ready` - Agente disponible
- `busy` - Agente procesando solicitud
- `error` - Agente con error
- `offline` - Agente no disponible

---

### 6. GET /health - Health Check

**Uso**: Verificar que la API está operacional

**Request**:
```
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "version": "1.0.0",
  "agents": {
    "total": 3,
    "ready": 3,
    "busy": 0,
    "error": 0
  }
}
```

---

## Tipos de Agentes Disponibles

### ingeniero_ti
- **Nombre**: Carlos Mendoza
- **Especialización**: Infraestructura TI, Linux, redes, seguridad
- **Casos de uso**: Configuración de servidores, troubleshooting, optimización
- **RAG**: Documentación técnica de Linux, Nginx, Apache, MySQL, PostgreSQL

### ingeniero_nube  
- **Nombre**: Ana García
- **Especialización**: Cloud computing, DevOps, containerización
- **Casos de uso**: Arquitectura cloud, costos AWS/Azure/GCP, Kubernetes, CI/CD
- **RAG**: Documentación de AWS, Azure, GCP, Docker, Kubernetes

### asesor_legal
- **Nombre**: María López
- **Especialización**: Derecho tecnológico, contratos IT, compliance
- **Casos de uso**: Revisión de contratos, GDPR, licencias, propiedad intelectual
- **RAG**: Legislación, precedentes, templates de contratos

---

## Flujo de Conversación

### Escenario: Usuario envía primer mensaje

1. **Frontend** → Usuario escribe mensaje y hace clic en "Enviar"

2. **api.py** → Función `send_message()` recibe el mensaje
   ```python
   @frappe.whitelist()
   def send_message(conversation, message, message_type="Text"):
       # Guardar mensaje del usuario en DB
       # Llamar a AgentService
   ```

3. **agent_service.py** → Clase `AgentService`
   ```python
   def get_response(self, message, conversation_id):
       # 1. Obtener o crear session_id
       session_id = self._get_or_create_session(conversation_id)
       
       # 2. Preparar payload
       payload = {
           "agent_type": "ingeniero_ti",
           "query": message,
           "session_id": session_id
       }
       
       # 3. Llamar a API
       response = requests.post("/chat", json=payload)
   ```

4. **Multi-Agent API** → Procesa la solicitud
   - Identifica el agente (`ingeniero_ti`)
   - Busca documentos relevantes (RAG)
   - Genera respuesta con LLM
   - Devuelve QueryResponse

5. **agent_service.py** → Procesa respuesta
   ```python
   result = response.json()
   response_text = result["response"]
   
   # Log token usage y sources
   return response_text
   ```

6. **api.py** → Guarda respuesta del agente
   ```python
   agent_message = frappe.get_doc({
       "doctype": "Chat Message",
       "sender_type": "Agent",
       "message": response
   })
   agent_message.insert()
   ```

7. **Frontend** → Muestra respuesta al usuario

---

## Gestión de Sesiones

### Creación Automática
```python
def _get_or_create_session(self, conversation_id):
    # 1. Buscar session_id en metadata de conversación
    conv = frappe.get_doc("Chat Conversation", conversation_id)
    metadata = json.loads(conv.metadata or '{}')
    
    if metadata.get('session_id'):
        return metadata['session_id']
    
    # 2. Crear nueva sesión via API
    response = requests.post("/sessions/new", json={
        "agent_type": self._get_agent_type(),
        "metadata": {"conversation_id": conversation_id}
    })
    
    session_id = response.json()['session_id']
    
    # 3. Guardar en metadata
    metadata['session_id'] = session_id
    conv.db_set('metadata', json.dumps(metadata))
    
    return session_id
```

### Persistencia
- `session_id` se almacena en `Chat Conversation.metadata`
- Formato: `{"session_id": "abc-123-def", "created_at": "..."}`
- Se reutiliza el mismo `session_id` para toda la conversación
- Permite mantener contexto entre múltiples intercambios

---

## Manejo de Errores

### Error de Conexión
```python
except requests.exceptions.ConnectionError:
    frappe.log_error("No se puede conectar con la API de agentes")
    frappe.throw(_("El servicio de agentes no está disponible"))
```

### Error HTTP 422 (Validación)
```python
except requests.exceptions.HTTPError as e:
    error_data = e.response.json()
    detail = error_data.get("detail", [])
    # detail[0]['msg'] contiene el mensaje de error
    frappe.throw(_("Error de validación: {0}").format(detail))
```

### Error HTTP 500 (Servidor)
```python
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 500:
        frappe.log_error("Error interno en API de agentes")
        frappe.throw(_("Error en el servicio de agentes"))
```

### Timeout
```python
except requests.exceptions.Timeout:
    frappe.throw(_("El agente tardó demasiado en responder"))
```

---

## Logging y Monitoreo

### Token Usage
```python
if "token_usage" in result:
    token_usage = result["token_usage"]
    frappe.logger().info(
        f"Tokens - Prompt: {token_usage['prompt_tokens']}, "
        f"Completion: {token_usage['completion_tokens']}, "
        f"Total: {token_usage['total_tokens']}"
    )
```

### RAG Sources
```python
if "sources" in result and result["sources"]:
    frappe.logger().info(f"RAG sources: {len(result['sources'])}")
    for source in result["sources"]:
        frappe.logger().debug(
            f"Source: {source['title']} "
            f"(relevance: {source['relevance']})"
        )
```

### Errores
```python
frappe.log_error(
    title="Agent API Error",
    message=f"Endpoint: {endpoint}\nPayload: {payload}\nError: {str(e)}"
)
```

---

## Configuración Avanzada

### Variables de Entorno en Agent

Cada Agent puede tener configuración específica:

```python
# En Agent DocType
{
    "api_endpoint": "http://localhost:8000/chat",
    "api_key": "optional-key",
    "temperature": 0.7,
    "max_tokens": 2000,
    "metadata": {
        "agent_type": "ingeniero_ti",
        "rag_enabled": true,
        "max_sources": 5
    }
}
```

### Prioridad de Configuración

1. Configuración en Agent (más alta prioridad)
2. site_config.json
3. Valores por defecto en el código

---

## Testing

### Test Unitario - Agent Service
```python
def test_agent_service():
    agent = frappe.get_doc("Agent", "Ingeniero TI")
    service = AgentService(agent.name)
    
    response = service.get_response(
        message="¿Cómo instalo Nginx?",
        conversation_id="CHAT-0001"
    )
    
    assert response
    assert len(response) > 0
```

### Test de Integración - API
```bash
# Health check
curl http://localhost:8000/health

# Listar agentes
curl http://localhost:8000/agents

# Consulta de prueba
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "ingeniero_ti",
    "query": "¿Cómo configuro SSH?"
  }'
```

---

## Mejores Prácticas

### 1. Reutilizar Sesiones
✅ Usar el mismo `session_id` para toda una conversación
❌ Crear nueva sesión para cada mensaje

### 2. Manejar Timeouts
✅ Configurar timeout de 30-60 segundos
❌ Dejar timeout indefinido

### 3. Log de Errores
✅ Usar `frappe.log_error()` con contexto completo
❌ Silenciar excepciones

### 4. Validar Responses
✅ Verificar que `response.json()` tenga el campo `response`
❌ Asumir estructura sin validar

### 5. Metadata en Agentes
✅ Almacenar `agent_type` en metadata JSON
❌ Hard-codear mapeos en el código

---

## Recursos Adicionales

- [OpenAPI Spec](./openapi.json) - Especificación completa de tu API
- [API_CONFIG.md](./API_CONFIG.md) - Guía de configuración
- [QUICKSTART.md](./QUICKSTART.md) - Inicio rápido
- [Frappe API Docs](https://frappeframework.com/docs/user/en/api) - Documentación de Frappe

---

**Última actualización**: Octubre 2025
**Versión API**: 1.0.0
**Compatibilidad**: Frappe v14+
