# Chat Frappe 🤖💬

Sistema de chat con agentes de IA multi-especializados para Frappe Framework.  
Integrado con API Multi-Agente personalizada con soporte RAG.

## 🌟 Características

- 🤖 **3 Agentes Especializados**: 
  - 💻 **Ingeniero TI** (Carlos Mendoza) - Infraestructura, redes, servidores
  - ☁️ **Ingeniero Nube** (Ana García) - AWS, Azure, GCP, Kubernetes
  - ⚖️ **Asesor Legal** (María López) - Contratos, GDPR, compliance
- 💬 **Interfaz tipo WhatsApp**: Chat intuitivo con lista de contactos
- 🔌 **API Multi-Agente**: Integración con tu API personalizada con RAG
- 📚 **RAG Enabled**: Respuestas basadas en documentos relevantes
- 🔄 **Gestión de Sesiones**: Mantiene contexto entre conversaciones
- 📱 **Responsive**: Funciona en desktop y móvil
- 🔒 **Seguro**: Sistema de permisos integrado de Frappe
- 📊 **Monitoreo**: Logging de token usage y fuentes RAG

## Instalación

### Opción 1: Desde el código local

```bash
# 1. Ve al directorio de apps de tu bench
cd ~/frappe-bench/apps

# 2. Clona o copia la aplicación
git clone https://github.com/tu-usuario/chat_frappe
# O crea un enlace simbólico: ln -s /ruta/a/chat_frappe chat_frappe

# 3. Instala la aplicación en tu sitio
cd ~/frappe-bench
bench --site tu-sitio.local install-app chat_frappe

# 4. Migra la base de datos
bench --site tu-sitio.local migrate

# 5. Reinicia bench
bench restart
```

### Opción 2: Desde repositorio remoto

```bash
cd ~/frappe-bench
bench get-app https://github.com/tu-usuario/chat_frappe
bench --site tu-sitio.local install-app chat_frappe
bench restart
```

Ver [INSTALL.md](INSTALL.md) para guía detallada.

## Uso

1. Accede a "Agent" y crea tus agentes de IA con sus configuraciones
2. Ve a "Chat" desde el menú principal
3. Selecciona un agente de la lista de contactos
4. ¡Comienza a chatear!

## Configuración de API Externa

Configura la URL de tu API de agentes en `Site Config`:

```json
{
  "chat_agent_api_url": "https://tu-api.com/agent",
  "chat_agent_api_key": "tu-api-key"
}
```

## Licencia

MIT
