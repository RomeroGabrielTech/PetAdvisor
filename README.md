
# Asistente de Mascotas 🐾 | Pet Care Assistant 🐾

[Español](#español) | [English](#english)

# Español

Un asistente virtual especializado en el cuidado de mascotas, con enfoque particular en el cuidado de pollos y otras mascotas comunes. Desarrollado con Flask y la API de OpenAI.

## Características
- Interfaz web intuitiva y responsive
- Respuestas generadas por IA usando GPT-3.5
- Diseño moderno con tema oscuro
- Soporte multilingüe (Español, Inglés, Francés y Portugués)
- Sistema de control de uso y notificaciones
- Registro detallado de consultas

## Tecnologías
- Python 3.10+
- Flask
- OpenAI API
- HTML/CSS
- Detección automática de idioma
- Sistema de notificaciones SMTP

## Configuración
1. Configura las variables de entorno en Replit:
   - OPENAI_API_KEY
   - EMAIL_USER
   - EMAIL_PASSWORD
2. Ejecuta el proyecto (puerto 8080)

## Sistema de Control
- Monitoreo de uso de tokens
- Notificaciones automáticas de límites
- Reportes periódicos por correo
- Registro completo de interacciones

---

# English

A virtual assistant specialized in pet care, with particular focus on chicken care and other common pets. Developed with Flask and OpenAI API.

## Features
- Intuitive and responsive web interface
- AI-generated responses using GPT-3.5
- Modern dark theme design
- Multilingual support (Spanish, English, French, Portuguese)
- Usage control and notification system
- Detailed query logging

## Technologies
- Python 3.10+
- Flask
- OpenAI API
- HTML/CSS
- Automatic language detection
- SMTP notification system

## Setup
1. Configure environment variables in Replit:
   - OPENAI_API_KEY
   - EMAIL_USER
   - EMAIL_PASSWORD
2. Run the project (port 8080)

## Control System
- Token usage monitoring
- Automatic limit notifications
- Periodic email reports
- Complete interaction logging

## Project Structure
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

## License
MIT License
