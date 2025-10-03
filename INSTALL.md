# Guía de Instalación - Chat Frappe

## Requisitos Previos

- Frappe Framework v14 o superior
- Python 3.10+
- Acceso a una API de agentes de IA

## Instalación

### 1. Obtener la aplicación

```bash
cd ~/frappe-bench
bench get-app https://github.com/tu-usuario/chat_frappe
```

O si tienes el código localmente:

```bash
cd ~/frappe-bench/apps
ln -s /ruta/a/chat_frappe chat_frappe
```

### 2. Instalar en tu sitio

```bash
bench --site tu-sitio.local install-app chat_frappe
```

### 3. Migrar la base de datos

```bash
bench --site tu-sitio.local migrate
```

### 4. Reiniciar bench

```bash
bench restart
```

## Configuración

### Configurar API de Agentes

Edita `site_config.json` de tu sitio:

```json
{
  "chat_agent_api_url": "https://api.openai.com/v1/chat/completions",
  "chat_agent_api_key": "tu-api-key-aqui"
}
```

O configura cada agente individualmente en el DocType "Agent".

### Formatos de API Soportados

La aplicación es compatible con APIs que siguen estos formatos de respuesta:

#### OpenAI Format
```json
{
  "choices": [
    {
      "message": {
        "content": "Respuesta del agente"
      }
    }
  ]
}
```

#### Simple Format
```json
{
  "response": "Respuesta del agente"
}
```

O

```json
{
  "message": "Respuesta del agente"
}
```

### Personalizar Agentes

1. Ve a **Agent** en el escritorio de Frappe
2. Los 3 agentes por defecto ya están creados:
   - Asistente General
   - Soporte Técnico
   - Analista de Datos
3. Edita o crea nuevos agentes con:
   - Nombre y descripción
   - Avatar personalizado
   - Endpoint de API específico (opcional)
   - API Key propia (opcional)
   - Temperature, Max Tokens
   - System Prompt personalizado

## Uso

### Acceder al Chat

1. Inicia sesión en tu sitio Frappe
2. Ve a **Chat** desde el menú principal
3. Selecciona un agente de la lista de contactos
4. ¡Comienza a chatear!

### Características

- **Múltiples Conversaciones**: Mantén conversaciones separadas con cada agente
- **Historial de Mensajes**: Todos los mensajes se guardan en la base de datos
- **Estado en Tiempo Real**: Indicadores de "escribiendo..."
- **Interfaz Responsive**: Funciona en desktop y móvil
- **Notificaciones**: Contador de mensajes no leídos

## Desarrollo

### Estructura del Proyecto

```
chat_frappe/
├── chat_frappe/
│   ├── doctype/
│   │   ├── agent/           # DocType para agentes
│   │   ├── chat_conversation/  # DocType para conversaciones
│   │   └── chat_message/    # DocType para mensajes
│   ├── chat_frappe/
│   │   └── page/
│   │       └── chat/        # Página principal del chat
│   ├── api.py              # API endpoints
│   ├── agent_service.py    # Servicio de integración con agentes
│   ├── install.py          # Scripts de instalación
│   └── public/
│       ├── js/
│       └── css/
├── hooks.py
├── pyproject.toml
└── README.md
```

### Extender la Funcionalidad

#### Agregar un nuevo tipo de mensaje

1. Edita `chat_message.json` y agrega el tipo en el campo `message_type`
2. Actualiza la UI en `chat.js` para renderizar el nuevo tipo
3. Actualiza la lógica en `api.py` si es necesario

#### Integrar con otro servicio de IA

1. Edita `agent_service.py`
2. Modifica el método `_call_agent_api()` para tu formato de API
3. Ajusta `_prepare_payload()` según los requisitos de tu API

## Troubleshooting

### Los mensajes no se envían

- Verifica que la API URL y Key estén configuradas correctamente
- Revisa los logs de error: `bench --site tu-sitio.local console`
- Comprueba la conexión de red a tu API de agentes

### Los agentes no aparecen

- Asegúrate de que la app esté instalada: `bench --site tu-sitio.local list-apps`
- Verifica que los fixtures se instalaron: `bench --site tu-sitio.local migrate`
- Crea agentes manualmente en el DocType "Agent"

### Errores de permisos

- Los roles "System Manager" y "All" tienen acceso por defecto
- Modifica los permisos en el DocType si necesitas restringir el acceso

## Soporte

Para reportar bugs o solicitar nuevas características, abre un issue en:
https://github.com/tu-usuario/chat_frappe/issues

## Licencia

MIT License - Ver LICENSE para más detalles
