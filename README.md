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

## 🎥 Demo del Proyecto

🌐 **Link al entorno de pruebas:** [gestoralum.onrender.com](https://gestoralum.onrender.com/)

## 🏗️ Arquitectura y Decisiones Técnicas

### Arquitectura de Software
El proyecto implementa el patrón arquitectónico **MVT (Model-View-Template)** propio de Django, con una sólida capa de lógica basada en roles:
*   **Role-Based Access Control (RBAC)**: Mediante decoradores y mixins personalizados se asegura de que cada usuario (Alumno, Profesor o Admin) interactúe únicamente con las vistas y datos correspondientes a su perfil.
*   **Desacoplamiento Lógico**: La separación de responsabilidades garantiza que la lógica de validación de negocio (ej. control de cupos o verificación de alumnos ya inscriptos) se mantenga en los Modelos/Formularios, manteniendo las Vistas limpias.

### Modelo de Datos (Entity-Relationship)
La base de datos fue diseñada en tercera forma normal (3NF) para evitar redundancias, asegurando integridad referencial con **PostgreSQL**:
*   **Gestión de Perfiles**: Extensión del modelo `User` nativo de Django usando relaciones `OneToOne` hacia las entidades `Alumno` y `Profesor`. Esto independiza la autenticación de la información académica.
*   **Entidades Académicas**: Separación entre `Materia` (definición global, ej: "Matemática 1") y `Comision` (grupos, ej: "Turno Mañana").
*   **Resolución Many-to-Many Flexible**: La entidad `MateriaComision` es el núcleo del sistema. Conecta una materia con una comisión específica y le define un `cupo_maximo`.
*   **Gestión Docente y Horarios**: Los horarios (`Horario`) y el cuerpo docente (`RolProfesor`: Titular/Ayudante) se vinculan a la instancia de `MateriaComision`, no a la Materia en sí, permitiendo total flexibilidad organizativa.
*   **Inscripciones e Historial**: La `Inscripcion` vincula a un `Alumno` con una `MateriaComision` y registra el `año_cursada`. Esto permite llevar un historial histórico de `nota` y condición (`aprobado`), manejando correctamente a los alumnos recursantes sin pisar datos de años anteriores.

### ¿Por qué Python y Django?
La elección de **Django** no fue azarosa. Su filosofía *"batteries included"* permitió:
1.  **Seguridad por Defecto**: Protección nativa contra inyecciones SQL, ataques XSS, CSRF y Clickjacking.
2.  **Productividad (Admin Panel)**: El uso del **Django Admin** facilitó desplegar el backend administrativo inmediatamente, focalizando el esfuerzo de desarrollo en los portales específicos de alumnos y profesores.
3.  **ORM Potente**: Gestión de relaciones complejas en la base de datos de forma programática y agnóstica al motor SQL subyacente.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Razón de elección |
| :--- | :--- | :--- |
| **Backend** | Python 3.11 / Django 5.1 | Madurez, escalabilidad y rapidez de desarrollo. |
| **Base de Datos** | PostgreSQL | Integridad referencial y soporte robusto para transacciones atómicas. |
| **Contenerización** | Docker & Docker Compose | Garantiza paridad absoluta entre entornos de desarrollo y producción. |
| **Frontend** | Django Templates / CSS3 / Bootstrap | Renderizado eficiente en el servidor y diseño responsive veloz. |
| **Servidor WSGI** | Gunicorn | Estándar de la industria para el despliegue de aplicaciones Python. |

---

## 🌟 Características Principales

### 👤 Perfil Alumno
- **Dashboard de Estadísticas**: Vista rápida de promedio histórico, materias aprobadas y en curso.
- **Inscripción Inteligente**: Buscador de materias, validación de cupos por comisión y prevención de doble inscripción anual.
- **Agenda de Horarios**: Calendario dinámico con los días y horarios de cursada.
- **Seguimiento Curricular**: Historial completo de calificaciones.

### 👨‍🏫 Perfil Profesor
- **Gestión de Comisiones**: Acceso directo a las listas de alumnos por materia y comisión asignada.
- **Carga de Notas**: Sistema ágil para calificar y monitorear el rendimiento del grupo, validando automáticamente la aprobación (>= 4).
- **Control de Actas**: Herramientas de visualización del estado del alumnado.

### 🔐 Administración (Superuser)
- **Gestión de Cuentas**: Alta, baja (soft-delete) y modificación de alumnos y docentes.
- **Configuración Académica**: Creación de materias, comisiones y asignación de roles docentes (Titular/Ayudante) con resolución de conflictos.

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

2.  **Configurar Variables de Entorno**:
    Crea un archivo `.env` en la raíz del proyecto basándote en el entorno.
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
    - App Principal: [http://localhost:8000](http://localhost:8000)
    - Panel Admin: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 📌 Roadmap / Futuras Mejoras
- [ ] Implementación de Reportes en PDF para certificados de alumno regular y analíticos.
- [ ] Módulo de Asistencia mediante escaneo de códigos QR.
- [ ] Notificaciones vía Email para alertas de inscripción y publicación de notas (Celery + Redis).
- [ ] Integración de API RESTful (Django REST Framework) para futura App Mobile.

---

Desarrollado con ❤️ por [JoacoM2003](https://github.com/JoacoM2003)