# Backend Stack Mis Eventos

Este proyecto fue desarrollado tomando como plantilla el full stack official de ⚡ FastApi [full-stack-fastapi-template
](https://github.com/fastapi/full-stack-fastapi-template/tree/master).

Este stack de backend permite administrar el ciclo de vida de un evento, desde su creación y configuración hasta la gestión de
asistentes.

## Stack de tecnologías

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) para la API del backend en Python.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) para la interacción entre Python y la base de datos SQL(ORM).
    - ⚙️ [Pydantic](https://docs.pydantic.dev), usado por FastAPI, para validación de datos and administración de configuraciones.
    - 🔨 [Poetry](https://python-poetry.org) para la gestión de paquetes y dependencias de Python.
    - 💾 [PostgreSQL](https://www.postgresql.org) como base de datos SQL.
    - 🔍 [Elasticsearch](https://www.elastic.co/elasticsearch) como motor de busqueda para la consulta de Eventos (No implementado).
    - 🚪 [GraphQL](https://graphql.org/), usado para la interacción entre la API y Elasticsearch (No implementado).
- 🐋 [Docker Compose](https://www.docker.com) para desarrollo.
- 🔒 Hashing de contraseñas por defecto.
- 🔑 Autenticación JWT (JSON Web Token).
- 📫 Recuperación de contraseñas basado en envio de Emails.
- ✅ Tests con [Pytest](https://pytest.org) (En progreso).

## Funcionalidades

- Registrar, leer, modificar y eliminar usuarios.
- Autenticación de usuarios usando JWT.
- Registrar, leer, modificar y eliminar eventos.
- Registrar, leer, modificar y eliminar sesiones correspondientes a los eventos existentes.
- Asignar usuarios como asistentes a los eventos.
- Asignar ponentes a las sesiones.
- Asignar usuarios como asistentes a las sesiones.

## Supuestos

- El usuario que cree el evento es asignado como el organizador del mismo.
- Cada evento puede tener solo una sesión en simultaneo.
- Cada sesión puede tener solo un ponente.

## Colección de Postman
El archivo Mis-Eventos-API.postman_collection.json es generado para probar los endpoints de la API desde Postman.
Contiene la colleción de endpoints de la API con su request y su respuesta.

## Configuración

Los parametros de configuración pueden ser actualizados y personalizados en el archivo `.env`.

La variables de entorno asociadas a contraseñas deberian ser enviadas como variables de entorno desde secrets:

- `SECRET_KEY`
- `FIRST_SUPERUSER_PASSWORD`
- `POSTGRES_PASSWORD`
- `POSTGRES_PASSWORD`
- `ES_PASSWORD`
- `RD_PASSWORD`

### Generación de Secret Keys

El valor por defecto de las variables anteriores debe ser modificado a una clave secreta, para generar las claves jecute el siguiente comando:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copie el contenido y uselo como contraseña/ clave secreta.

## Desarrollo

### Ejecución

Inicie el entorno de desarrollo local con Docker Compose:
```bash
docker compose watch
```

* Se puede interactuar con el backend desde la URL http://localhost:8000

Para ver los logs de todo el stack, ejecute en una nueva terminal:

```bash
docker compose logs
```

Paar ver los logs correspondientes al servicio de backend:

```bash
docker compose logs backend
```
### Desarrollo del Backend

Documentación del Backend: [backend/README.md](./backend/README.md).

## Trabajo futuro

- Validar la capacidad de asistentes en eventos y sesiones
- Integrar busqueda de eventos por Elasticsearch
- Integrar sincronización de Elasticsearch con Postgres usando [PGSync](https://pgsync.com/)
- Integrar funcionalidad para gestión de cache usando Redis (El entorno de Redis ya se encuentra añadido al stack de Docker Compose).
- Integrar sistema de notificaciones
- Integrar sistema de reporte y análitica
