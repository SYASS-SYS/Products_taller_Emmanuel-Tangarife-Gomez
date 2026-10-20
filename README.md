# CompraFácil — Gestión de compras con Django

Aplicación web para registrar proveedores y compras. Proyecto pensado para principiantes y preparado para usar PostgreSQL en Neon y publicar en Render.

## Funciones incluidas

- Inicio y cierre de sesión con la autenticación de Django.
- Páginas administrativas protegidas: no se ven sin iniciar sesión.
- CRUD de proveedores: crear, consultar, editar y eliminar si no tiene compras relacionadas.
- CRUD de compras: crear, consultar, editar estado/datos y eliminar.
- Cada compra queda vinculada al proveedor y al usuario que la registró.
- Búsqueda de proveedores por nombre o NIT.
- Filtros de compras por proveedor y estado.
- Validaciones en JavaScript y repetidas en Django; NIT y número de compra únicos.
- Interfaz adaptable con Bootstrap.
- SQLite para probar localmente y PostgreSQL cuando se configura `DATABASE_URL`.

## 1. Ejecutar en tu computador

Necesitas Python 3.11 o superior.

### Windows

Abre la terminal en la carpeta del proyecto y ejecuta:

```powershell
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abre http://127.0.0.1:8000 y entra con el usuario que acabas de crear. Si usas PowerShell y no te deja activar el entorno, puedes ejecutar `venv\Scripts\python.exe -m pip install -r requirements.txt` y luego `venv\Scripts\python.exe manage.py runserver`.

## 2. Crear la base de datos en Neon

1. Entra en https://neon.tech/ y crea un proyecto PostgreSQL.
2. Copia la cadena de conexión de PostgreSQL que ofrece Neon. Debe empezar por `postgresql://` o `postgres://`.
3. En Render, esa cadena se guardará como variable de entorno `DATABASE_URL`; no la pegues en archivos del proyecto ni la subas a GitHub.

Si la cadena de conexión tiene `sslmode=require`, déjalo incluido.

## 3. Subir a GitHub

1. Crea un repositorio vacío en GitHub.
2. Desde la carpeta del proyecto, ejecuta:

```bash
git init
git add .
git commit -m "Primera version de CompraFacil"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/TU-REPOSITORIO.git
git push -u origin main
```

Reemplaza la URL de ejemplo por la de tu repositorio. No subas claves ni la cadena de conexión de Neon.

## 4. Publicar en Render

1. En https://render.com/ selecciona **New + → Web Service** y conecta tu repositorio.
2. Render detectará la configuración de `render.yaml`. Si configuras el servicio manualmente, usa:
   - **Runtime:** Python
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn config.wsgi:application`
3. En **Environment**, agrega `DATABASE_URL` con la cadena de conexión de Neon.
4. Comprueba que existan `SECRET_KEY` (un valor secreto), `DEBUG=false` y, si es necesario, `ALLOWED_HOSTS` con el dominio de tu aplicación sin `https://`.
5. Inicia el despliegue. `build.sh` instala las dependencias, recoge los archivos estáticos y ejecuta las migraciones.
6. Cuando el servicio esté desplegado, crea el usuario administrador desde **Render → servicio → Shell** con:

```bash
python manage.py createsuperuser
```

Si tu tipo de servicio de Render no incluye Shell, ejecuta `python manage.py createsuperuser` temporalmente desde una consola con la misma `DATABASE_URL`, o crea un usuario administrador mediante una tarea de consola que use las variables de entorno del servicio. No pongas la contraseña en el código.

## 5. Prueba rápida

1. Inicia sesión.
2. Crea un proveedor con NIT, contacto, teléfono, correo y dirección.
3. Crea una compra asociada a ese proveedor.
4. Cambia el estado de la compra a recibida o cancelada.
5. Busca el proveedor por nombre/NIT y filtra compras por estado/proveedor.
6. Comprueba que no se puede guardar un NIT o número de compra duplicado.
7. Intenta eliminar un proveedor con compras: la aplicación debe impedirlo.
8. Cierra sesión e intenta abrir una ruta interna: debe redirigir al inicio de sesión.

## Estructura de carpetas

```text
comprafacil/
├── config/                 # Configuración principal de Django
├── gestion/                # Modelos, formularios, vistas y URLs
│   ├── static/gestion/     # CSS y JavaScript
│   └── templates/gestion/  # HTML de las pantallas
├── build.sh                # Instalación y migraciones en Render
├── render.yaml             # Configuración de despliegue
├── manage.py
└── requirements.txt
```

## Notas para principiantes

- `models.py`: define las tablas Proveedor y Compra.
- `forms.py`: valida datos de formularios en el servidor.
- `views.py`: contiene la lógica de cada pantalla.
- `urls.py`: relaciona las direcciones con las vistas.
- `templates/`: contiene el HTML.
- `validaciones.js`: muestra errores de formulario en el navegador; las validaciones de Django siguen siendo obligatorias.
- `settings.py`: usa SQLite en local si no existe `DATABASE_URL` y PostgreSQL en producción cuando la variable está configurada.

El proyecto no incluye productos, inventario, detalle de compra ni API REST porque no son requeridos por el documento de práctica.
