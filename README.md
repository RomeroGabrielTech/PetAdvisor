
# Asistente de Mascotas 🐾

Un asistente virtual especializado en el cuidado de mascotas, con enfoque particular en el cuidado de pollos y otras mascotas comunes. Desarrollado con Flask y la API de OpenAI.

## Características

- Interfaz web intuitiva y responsive
- Respuestas generadas por IA usando GPT-3.5
- Diseño moderno con tema oscuro
- Registro de conversaciones
- Validación de entrada de usuario
- Soporte multilingüe (Español, Inglés, Francés y Portugués)
- Detección automática del idioma de entrada
- Control de uso de tokens de OpenAI
- Sistema de notificaciones por correo
- Reportes de uso automáticos

## Tecnologías Utilizadas

- Python 3.10+
- Flask
- OpenAI API
- HTML/CSS
- Langdetect (para detección de idiomas)
- SMTP (para notificaciones por correo)

## Configuración

1. Asegúrate de tener una clave API de OpenAI
2. Configura las variables de entorno en Replit:
   - OPENAI_API_KEY: Tu clave de API de OpenAI
   - EMAIL_USER: Tu correo Gmail
   - EMAIL_PASSWORD: Tu contraseña de aplicación de Gmail
3. El proyecto se ejecutará automáticamente en el puerto 8080

## Uso

1. Accede a la página principal
2. Escribe tu pregunta en cualquier idioma soportado (ES/EN/FR/PT)
3. El sistema detectará automáticamente el idioma
4. Recibe una respuesta detallada y práctica en el mismo idioma
5. Consulta el historial en log.txt

## Control de Uso

- Límite configurable de tokens de OpenAI
- Notificaciones automáticas al alcanzar el límite
- Reportes periódicos de uso por correo
- Registro detallado de todas las consultas

## Estructura del Proyecto

```
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   └── response.html
├── main.py
├── log.txt
└── README.md
```

## Licencia

Este proyecto está bajo la Licencia MIT.
