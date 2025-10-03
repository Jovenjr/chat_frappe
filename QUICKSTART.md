# 🚀 Quick Start - Chat Frappe

## Instalación Rápida (3 pasos)

```bash
# 1. Copiar la app a tu bench
cd ~/frappe-bench/apps
ln -s /c/Proyectos/chat_frappe chat_frappe

# 2. Instalar en tu sitio
cd ~/frappe-bench
bench --site tu-sitio.local install-app chat_frappe
bench --site tu-sitio.local migrate

# 3. Reiniciar y listo!
bench restart
```

## Configuración Mínima

Edita `sites/tu-sitio.local/site_config.json`:

```json
{
  "chat_agent_api_url": "http://localhost:8000",
  "chat_agent_api_key": "tu-api-key-opcional"
}
```

**Nota**: Asegúrate de que tu API Multi-Agente esté corriendo en el puerto 8000 (o ajusta la URL según corresponda).

## Acceder al Chat

1. Abre tu navegador: `http://tu-sitio.local`
2. Inicia sesión
3. Ve al módulo **"Chat"** o directamente a: `http://tu-sitio.local/app/chat`
4. Verás 3 agentes en la barra lateral:
   - 💻 **Ingeniero TI** (Carlos Mendoza) - Infraestructura y Servidores
   - ☁️ **Ingeniero Nube** (Ana García) - AWS, Azure, GCP, Kubernetes
   - ⚖️ **Asesor Legal** (María López) - Contratos y Cumplimiento
5. Haz clic en uno y ¡comienza a chatear!

## Primera Conversación

### Ejemplo con Ingeniero TI:
```
Usuario: ¿Cómo configuro Nginx con SSL?
Ingeniero TI (Carlos): Para configurar Nginx con SSL, necesitas:
1. Obtener un certificado SSL (Let's Encrypt es gratis)
2. Configurar el bloque server en /etc/nginx/sites-available/...
[Respuesta detallada con comandos y ejemplos]
```

### Ejemplo con Ingeniero Nube:
```
Usuario: ¿Cuánto costaría migrar mi app a AWS?
Ingeniero Nube (Ana): Para estimar los costos de AWS, necesito saber:
- Tráfico mensual esperado
- Tamaño de la base de datos
- Requerimientos de storage
[Análisis detallado de costos y recomendaciones]
```

### Ejemplo con Asesor Legal:
```
Usuario: ¿Qué cláusulas debe tener un contrato SaaS?
Asesor Legal (María): Un contrato SaaS debe incluir:
1. Definición de servicios y SLA
2. Propiedad intelectual
3. Protección de datos (GDPR)
[Asesoría legal completa]
```

## Personalizar Agentes

1. Ve a: **Agent** en el escritorio
2. Edita cualquiera de los 3 agentes o crea nuevos
3. Personaliza:
   - **Avatar**: Sube una imagen
   - **System Prompt**: Define su personalidad
   - **Temperature**: 0-1 (creatividad)
   - **API Config**: Endpoint y key específicos

## Tu API Multi-Agente

La aplicación está configurada para trabajar con tu API personalizada de agentes.

### Características de tu API:

✅ **3 Agentes Especializados:**
- `ingeniero_ti` - Carlos Mendoza (Infraestructura TI)
- `ingeniero_nube` - Ana García (Cloud & DevOps)  
- `asesor_legal` - María López (Legal Tech)

✅ **Soporte RAG (Retrieval-Augmented Generation):**
- Respuestas basadas en documentos
- Referencias a fuentes
- Contexto relevante automático

✅ **Gestión de Sesiones:**
- Mantiene contexto entre mensajes
- Historial de conversación completo
- Session IDs automáticos

✅ **Endpoints Disponibles:**
- `/chat` - Conversación con agentes
- `/query` - Consultas directas
- `/sessions/new` - Crear sesión
- `/sessions/{id}/history` - Ver historial
- `/agents` - Listar agentes disponibles
- `/health` - Health check

Ver [API_CONFIG.md](API_CONFIG.md) para documentación completa de la API.

## Estructura del Proyecto

```
chat_frappe/
├── hooks.py                    # Configuración
├── chat_frappe/
│   ├── api.py                  # Endpoints REST
│   ├── agent_service.py        # Integración con IA
│   ├── doctype/                # Modelos de datos
│   │   ├── agent/
│   │   ├── chat_conversation/
│   │   └── chat_message/
│   └── page/
│       └── chat/               # Interfaz UI
└── config/                     # Módulo del escritorio
```

## Troubleshooting

### ❌ App no aparece en el escritorio
```bash
bench --site tu-sitio.local clear-cache
bench restart
```

### ❌ Agentes no aparecen
```bash
bench --site tu-sitio.local console
>>> from chat_frappe.install import install_agents
>>> install_agents()
```

### ❌ Error al enviar mensajes
- Verifica tu API key en `site_config.json`
- Revisa los logs: `tail -f ~/frappe-bench/sites/tu-sitio.local/logs/web.log`

### ❌ Error de imports
```bash
# Reinstalar la app
bench --site tu-sitio.local uninstall-app chat_frappe
bench --site tu-sitio.local install-app chat_frappe
bench --site tu-sitio.local migrate
```

## Comandos Útiles

```bash
# Ver logs en tiempo real
tail -f ~/frappe-bench/sites/tu-sitio.local/logs/web.log

# Console de Python
bench --site tu-sitio.local console

# Ejecutar tests
bench --site tu-sitio.local run-tests --app chat_frappe

# Limpiar cache
bench --site tu-sitio.local clear-cache

# Rebuild assets
bench build --app chat_frappe

# Backup del sitio
bench --site tu-sitio.local backup
```

## Desarrollo

### Agregar un nuevo agente

1. Ve a **Agent** → **New**
2. Completa:
   - **Agent Name**: Mi Nuevo Agente
   - **Agent Type**: Custom
   - **Description**: Descripción corta
   - **API Endpoint**: `http://localhost:8000/chat`
   - **System Prompt**: Define su comportamiento
   - **Metadata**: `{"agent_type": "ingeniero_ti"}` (usa uno de los 3 tipos disponibles)
3. **Save**
4. El agente aparecerá automáticamente en el chat

**Nota**: Los tipos de agente disponibles en tu API son:
- `ingeniero_ti`
- `ingeniero_nube`
- `asesor_legal`

### Modificar la UI

Edita: `chat_frappe/page/chat/chat.js`

```javascript
// Personalizar colores
.chat-contact-item.active {
    background: #tu-color-aqui;
}
```

Rebuild:
```bash
bench build --app chat_frappe
```

## Documentación Completa

- 📖 [README.md](README.md) - Visión general
- 📦 [STRUCTURE.md](STRUCTURE.md) - Estructura del proyecto
- ⚙️ [API_CONFIG.md](API_CONFIG.md) - Configuración de APIs
- 🔧 [INSTALL.md](INSTALL.md) - Guía de instalación detallada
- ✅ [CHECKLIST.md](CHECKLIST.md) - Lista de verificación

## Soporte

¿Problemas? Abre un issue en GitHub o consulta la documentación de Frappe:
- https://frappeframework.com/docs

## Licencia

MIT License - Úsalo libremente en tus proyectos!

---

**¡Disfruta chateando con tus agentes de IA! 🎉**
