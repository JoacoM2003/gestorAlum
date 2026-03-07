# 🎓 GestorAlum: Sistema Integral de Gestión Académica

[![Django](https://img.shields.io/badge/Framework-Django%205.1-092e20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Language-Python%203.11-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ed?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

**GestorAlum** es una plataforma robusta y escalable diseñada para centralizar la administración académica. Desde la gestión de inscripciones hasta el seguimiento de calificaciones, el sistema ofrece una experiencia fluida tanto para administradores como para docentes y alumnos.

---

## 🎯 ¿Qué resuelve este proyecto?

En entornos académicos, la dispersión de la información en planillas de cálculo suele generar errores y duplicidad. **GestorAlum** resuelve:
*   **Gestión Centralizada**: Un único punto de verdad para datos personales, académicos y horarios.
*   **Automatización de Inscripciones**: Control de cupos en tiempo real para materias y comisiones.
*   **Transparencia Académica**: Dashboards personalizados para alumnos con promedios y estados de cursada automáticos.
*   **Eficiencia Docente**: Simplificación de la carga de notas y gestión de actas de cursada.

---

## 🏗️ Decisiones Técnicas y Arquitectura

### ¿Por qué Python y Django?
La elección de **Django** no fue azarosa. Su filosofía *"batteries included"* permitió:
1.  **Seguridad por Defecto**: Protección contra inyecciones SQL, XSS y CSRF nativa.
2.  **Productividad**: El uso del **Django Admin** permitió desplegar el backend administrativo en tiempo récord, permitiendo enfocarse en la lógica de negocio personalizada.
3.  **ORM Potente**: Gestión de relaciones complejas (Many-to-Many entre Materias y Comisiones) de forma intuitiva y segura.

### Arquitectura de Software
El proyecto implementa un patrón **MVT (Model-View-Template)** con una capa adicional de lógica basada en roles:
*   **Modelos Extensibles**: Se utilizó una relación `OneToOne` con el modelo `User` de Django para crear perfiles de `Alumno` y `Profesor` sin comprometer la integridad del sistema de autenticación estándar.
*   **Role-Based Access Control (RBAC)**: Decoradores personalizados y validaciones en vistas aseguran que cada usuario solo acceda a la información pertinente a su rol.
*   **Desacoplamiento Académico**: La relación `MateriaComision` actúa como puente, permitiendo que una materia sea dictada en múltiples horarios y por distintos profesores de forma flexible.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Razón de elección |
| :--- | :--- | :--- |
| **Backend** | Python 3.11 / Django 5.1 | Madurez, escalabilidad y rapidez de desarrollo. |
| **Base de Datos** | PostgreSQL | Integridad referencial y soporte robusto para transacciones atómicas. |
| **Contenerización** | Docker & Docker Compose | Garantiza paridad absoluta entre entornos de desarrollo y producción. |
| **Frontend** | Django Templates / CSS3 | Renderizado eficiente en el servidor y optimización SEO. |
| **Servidor WSGI** | Gunicorn | Estándar de la industria para el despliegue de aplicaciones Python. |

---

## 🌟 Características Principales

### 👤 Perfil Alumno
- **Dashboard de Estadísticas**: Vista rápida de promedio, materias aprobadas y cursando.
- **Inscripción Inteligente**: Buscador de materias y validación de cupos por comisión.
- **Agenda de Horarios**: Calendario dinámico con los días y horarios de cursada.
- **Seguimiento Curricular**: Historial completo de calificaciones.

### 👨‍🏫 Perfil Profesor
- **Gestión de Comisiones**: Acceso directo a las listas de alumnos por materia asignada.
- **Carga de Notas**: Sistema ágil para calificar y monitorear el rendimiento del grupo.
- **Limpieza de Actas**: Herramientas para depurar inscripciones sin calificación.

### 🔐 Administración (Superuser)
- **Gestión de Cuentas**: Alta, baja y modificación de alumnos y docentes.
- **Configuración Académica**: Creación de materias, comisiones y asignación de roles docentes (Titular/Ayudante).

---

## 🚀 Instalación y Despliegue Local

### Requisitos Previos
- Docker y Docker Compose instalados.

### Pasos:
1.  **Clonar el repositorio**:
    ```bash
    git clone https://github.com/JoacoM2003/gestorAlum.git
    cd gestorAlum
    ```

2.  **Configurar Variables de Envorno**:
    Crea un archivo `.env` en la raíz del proyecto.
    ```env
    DEBUG=True
    SECRET_KEY=tu_clave_secreta_aqui
    DATABASE_URL=postgres://postgres:admin@db:5432/gestorAlum
    ```

3.  **Encender Motores**:
    ```bash
    docker-compose up --build
    ```

4.  **Inicializar Base de Datos**:
    En una nueva terminal, ejecuta las migraciones y crea el usuario administrador:
    ```bash
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    ```

5.  **Acceso**:
    - App: [http://localhost:8000](http://localhost:8000)
    - Admin: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 📌 Roadmap / Futuras Mejoras
- [ ] Implementación de Reportes en PDF para certificados de alumno regular.
- [ ] Módulo de Asistencia mediante códigos QR.
- [ ] Notificaciones vía Email para alertas de inscripción y publicación de notas.
- [ ] Integración de API RESTful para futura App Mobile.

---

Desarrollado con ❤️ por [JoacoM2003](https://github.com/JoacoM2003)