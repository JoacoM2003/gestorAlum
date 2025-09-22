# 📚 GestorAlum

**GestorAlum** es una aplicación web desarrollada con Django, diseñada para gestionar información de estudiantes, incluyendo sus datos personales, notas y asistencia. Esta herramienta facilita el seguimiento académico y administrativo de los alumnos.

## 🛠️ Tecnologías

- **Backend:** Python 3.11, Django
- **Frontend:** HTML, CSS
- **Contenerización:** Docker
- **Base de datos:** PostgreSQL

## 🚀 Instalación

1. Clona el repositorio:

\`\`\`bash
git clone https://github.com/JoacoM2003/gestorAlum.git
cd gestorAlum
\`\`\`

2. Construye y ejecuta los contenedores con Docker:

\`\`\`bash
docker-compose up --build
\`\`\`

3. Accede a la aplicación en tu navegador:

\`\`\`
http://localhost:8000
\`\`\`

## 🔧 Estructura del Proyecto

- `gestor/`: Aplicación principal para la gestión de alumnos.
- `gestorAlum/`: Configuración del proyecto Django.
- `Dockerfile`: Configuración del contenedor.
- `docker-compose.yml`: Orquestación de servicios.
- `manage.py`: Herramienta de administración de Django.
- `requirements.txt`: Dependencias de Python.

## 🧪 Uso

- **Crear superusuario:**

\`\`\`bash
docker-compose exec web python manage.py createsuperuser
\`\`\`

- **Acceder al panel de administración:**

\`\`\`
http://localhost:8000/admin
\`\`\`

- **Agregar y gestionar alumnos, notas y asistencia** desde el panel de administración.

## 🌟 Características

- Gestión de datos personales de alumnos.
- Registro y seguimiento de notas y calificaciones.
- Control de asistencia.
- Panel de administración completo para superusuarios.
- Sistema modular con varias apps de Django.

## 🎬 Demo

Puedes ver una demo del proyecto en funcionamiento en el siguiente enlace:

[Demo del GestorAlum](https://gestoralum.onrender.com/)  

> *(Si tienes un hosting o URL real para la demo, reemplaza este link por el de la demo en línea)*

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulte el archivo LICENSE para más detalles.
