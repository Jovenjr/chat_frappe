# Ejemplo de Configuración de API

## Configuración Global (site_config.json)

Para tu API Multi-Agente personalizada:

```json
{
  "db_name": "tu_base_de_datos",
  "db_password": "tu_password",
  
  "chat_agent_api_url": "http://localhost:8000/chat",
  "chat_agent_api_key": "tu-api-key-opcional"
}
```

**Nota**: La URL debe apuntar a la raíz de tu API. El sistema automáticamente usará los endpoints `/chat`, `/sessions/new`, etc.

## Configuración por Agente

Cada agente puede tener su propia configuración. Edita el agente en Frappe:

### Tu API Multi-Agente (Configuración Recomendada)

- **API Endpoint**: `http://localhost:8000/chat` (o tu URL de producción)
- **API Key**: (opcional, si tu API lo requiere)
- **Temperature**: `0.7`
- **Max Tokens**: `2000`
- **Metadata**: `{"agent_type": "ingeniero_ti"}` (ver tipos disponibles abajo)

### Tipos de Agentes Disponibles

Según tu API, estos son los tipos disponibles:

1. **ingeniero_ti** - Carlos Mendoza (Infraestructura TI)
2. **ingeniero_nube** - Ana García (Cloud & DevOps)
3. **asesor_legal** - María López (Legal & Contratos)

### Ejemplo de Configuración en Frappe

**Ingeniero TI:**
- API Endpoint: `http://localhost:8000/chat`
- Metadata: `{"agent_type": "ingeniero_ti"}`
- System Prompt: "Eres Carlos Mendoza, experto en infraestructura TI..."

**Ingeniero Nube:**
- API Endpoint: `http://localhost:8000/chat`
- Metadata: `{"agent_type": "ingeniero_nube"}`
- System Prompt: "Eres Ana García, experta en cloud..."

**Asesor Legal:**
- API Endpoint: `http://localhost:8000/chat`
- Metadata: `{"agent_type": "asesor_legal"}`
- System Prompt: "Eres María López, asesora legal..."

## Formato de Request - Tu API Multi-Agente

La aplicación envía requests POST al endpoint `/chat` con este formato:

### QueryRequest (Endpoint: /chat o /query)

```json
{
  "agent_type": "ingeniero_ti",
  "query": "¿Cómo configuro un servidor Nginx con SSL?",
  "session_id": "abc-123-def-456",
  "context": {
    "system_prompt": "Eres un asistente experto...",
    "temperature": 0.7,
    "max_tokens": 2000
  }
}
```

### Creación de Sesión (Endpoint: /sessions/new)

La aplicación automáticamente crea sesiones para mantener el contexto:

```json
{
  "agent_type": "ingeniero_ti",
  "metadata": {
    "conversation_id": "CHAT-0001",
    "agent_name": "Ingeniero TI"
  }
}
```

## Formato de Response - Tu API Multi-Agente

### QueryResponse (respuesta de /chat o /query)

Tu API devuelve este formato, que la aplicación procesa automáticamente:

```json
{
  "agent_type": "ingeniero_ti",
  "response": "Para configurar Nginx con SSL, primero necesitas...",
  "session_id": "abc-123-def-456",
  "timestamp": "2024-01-01T12:00:00",
  "token_usage": {
    "prompt_tokens": 150,
    "completion_tokens": 300,
    "total_tokens": 450
  },
  "metadata": {
    "model": "gpt-4",
    "temperature": 0.7
  },
  "sources": [
    {
      "title": "Guía Nginx SSL",
      "relevance": 0.95,
      "url": "https://..."
    }
  ]
}
```

### SessionResponse (respuesta de /sessions/new)

```json
{
  "session_id": "abc-123-def-456",
  "agent_type": "ingeniero_ti",
  "created_at": "2024-01-01T12:00:00"
}
```

### ConversationHistory (respuesta de /sessions/{session_id}/history)

```json
{
  "session_id": "abc-123-def-456",
  "agent_type": "ingeniero_ti",
  "messages": [
    {
      "role": "user",
      "content": "¿Cuánto cuesta AWS?",
      "timestamp": "2024-01-01T12:00:00"
    },
    {
      "role": "assistant",
      "content": "Los costos de AWS varían...",
      "timestamp": "2024-01-01T12:00:05"
    }
  ],
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:05"
}
```

## Endpoints de Tu API Disponibles

Tu API Multi-Agente proporciona los siguientes endpoints:

### 1. `/health` - Health Check
```bash
GET http://localhost:8000/health
```

### 2. `/agents` - Listar Agentes
```bash
GET http://localhost:8000/agents
```
Respuesta:
```json
{
  "ingeniero_ti": {
    "name": "Carlos Mendoza",
    "description": "Ingeniero TI especializado en...",
    "status": "ready"
  },
  "ingeniero_nube": {...},
  "asesor_legal": {...}
}
```

### 3. `/agents/{agent_type}/status` - Estado del Agente
```bash
GET http://localhost:8000/agents/ingeniero_ti/status
```

### 4. `/query` o `/chat` - Consultar Agente
```bash
POST http://localhost:8000/chat
Content-Type: application/json

{
  "agent_type": "ingeniero_ti",
  "query": "¿Cómo configuro SSH?",
  "session_id": "optional-session-id"
}
```

### 5. `/sessions/new` - Crear Sesión
```bash
POST http://localhost:8000/sessions/new
Content-Type: application/json

{
  "agent_type": "ingeniero_ti",
  "metadata": {"user": "john"}
}
```

### 6. `/sessions/{session_id}/history` - Historial
```bash
GET http://localhost:8000/sessions/abc-123-def/history
```

### 7. `/sessions/{session_id}` - Eliminar Sesión
```bash
DELETE http://localhost:8000/sessions/abc-123-def
```

## Configuración Avanzada

### System Prompts Personalizados

Edita cada agente y personaliza su System Prompt:

**Ingeniero TI (Carlos Mendoza):**
```
Eres Carlos Mendoza, ingeniero TI experto con 10+ años de experiencia.
Especializaciones: Linux, Windows Server, Nginx, Apache, MySQL, PostgreSQL, redes, seguridad.
Ayudas con configuración de servidores, troubleshooting, optimización y mejores prácticas.
Responde de manera técnica pero clara, con ejemplos de comandos cuando sea apropiado.
```

**Ingeniero Nube (Ana García):**
```
Eres Ana García, ingeniera de nube con certificaciones en AWS, Azure y GCP.
Especializaciones: Kubernetes, Docker, Terraform, CI/CD, arquitectura serverless, microservicios.
Ayudas con diseño de arquitecturas cloud, optimización de costos, DevOps y migración a la nube.
Proporciona soluciones escalables y siguiendo las mejores prácticas de cada proveedor.
```

**Asesor Legal (María López):**
```
Eres María López, asesora legal especializada en tecnología y derecho digital.
Especializaciones: Contratos IT, GDPR, propiedad intelectual, licencias de software, compliance.
Ayudas con revisión de contratos, cumplimiento legal, protección de datos y regulaciones.
Proporciona asesoría clara y citas referencias legales cuando es relevante.
Nota: Siempre recomienda consultar con un abogado para casos específicos.
```

### Configuración de Metadata en Agentes

El campo `metadata` en cada Agent permite configuración adicional en formato JSON:

```json
{
  "agent_type": "ingeniero_ti",
  "rag_enabled": true,
  "max_sources": 5,
  "custom_settings": {
    "expertise_areas": ["linux", "docker", "nginx"],
    "response_style": "detailed"
  }
}
```

### Variables de Entorno / Site Config

Además de configurar en cada agente, puedes usar `site_config.json`:

```json
{
  "chat_agent_api_url": "http://localhost:8000",
  "chat_agent_api_key": "tu-api-key-opcional",
  "chat_default_temperature": 0.7,
  "chat_default_max_tokens": 2000,
  "chat_session_timeout": 3600
}
```

### Características RAG (Retrieval-Augmented Generation)

Tu API soporta RAG. Las respuestas pueden incluir `sources` con documentos relevantes:

```json
{
  "response": "Para configurar Nginx...",
  "sources": [
    {
      "title": "Guía Nginx SSL",
      "relevance": 0.95,
      "content": "...",
      "metadata": {...}
    }
  ]
}
```

La aplicación automáticamente registra en logs cuando se usan fuentes RAG.

### Gestión de Sesiones

- Las sesiones se crean automáticamente al iniciar una conversación
- El `session_id` se guarda en el campo `metadata` de Chat Conversation
- Las sesiones permiten mantener contexto entre múltiples mensajes
- Puedes ver el historial completo usando el endpoint `/sessions/{id}/history`

### Monitoreo y Logs

La aplicación registra automáticamente:
- Token usage (prompt, completion, total)
- Fuentes RAG utilizadas
- Errores de API con detalles completos
- Tiempos de respuesta

Ver logs en:
```bash
tail -f ~/frappe-bench/sites/tu-sitio.local/logs/web.log
```
