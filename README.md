# Backend IoT – UniverseThings / AgroDrone

Este backend está construido con **FastAPI + SQLAlchemy + MySQL** y está pensado para ejecutarse en local con **MySQL Workbench**.



## Prerrequisitos
Antes de empezar, nstala:

- **Python 3.10+**
- **MySQL 8.x**
- **MySQL Workbench**
- **Git**

Opcional pero recomendado:

- VS Code o IDE similar.

## Clonar el proyecto
```bash
git clone https://github.com/Solution-Development-IOT-Project/UniverseThings-Backend.git
cd UniverseThings-Backend/backend_structure_only
````


## Configurar MySQL y la base de datos (MySQL Workbench)
Abre **MySQL Workbench**.

Conéctate a tu servidor local (por ejemplo, `Local instance MySQL`).

Crea la base de datos del proyecto:

   ```sql
   CREATE DATABASE IF NOT EXISTS agrodrone_db
     DEFAULT CHARACTER SET utf8mb4
     DEFAULT COLLATE utf8mb4_unicode_ci;
   ```
Usar el usuario `root` (simple para desarrollo):

Asegúrate de recordar la contraseña de `root` (ejemplo: `admin`).
Si llegas a tener problemas con el plugin de autenticación (`caching_sha2_password`), puedes forzar `mysql_native_password`:

     ```sql
     ALTER USER 'root'@'localhost'
       IDENTIFIED WITH mysql_native_password BY 'TU_PASSWORD_AQUI';
     FLUSH PRIVILEGES;
     ```

ó 
Crear un usuario específico para el proyecto:


   ```sql
   CREATE USER 'agro_user'@'localhost'
     IDENTIFIED WITH mysql_native_password BY 'agro_pass';

   GRANT ALL PRIVILEGES ON agrodrone_db.* TO 'agro_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

Apunta bien estos datos porque se usan en la cadena de conexión del `.env`.



## Crear el archivo `.env`

En la carpeta `backend_structure_only` hay un archivo `.env` con contenido similar:

```env
# Nombre de la app
APP_NAME="UniverseThings Backend"

# Prefijo de la API
API_V1_STR=/api/v1

# Conexión a MySQL (ajusta usuario/contraseña/BD según tu caso)
# Ejemplo usando root:
# SQLALCHEMY_DATABASE_URL="mysql+pymysql://root:admin@localhost:3306/agrodrone_db"

# Ejemplo usando agro_user:
SQLALCHEMY_DATABASE_URL="mysql+pymysql://agro_user:agro_pass@localhost:3306/agrodrone_db"

# Clave para JWT (cambia esto en producción)
SECRET_KEY="cambia-esta-clave-por-una-mas-segura"

# Expiración del token (minutos)
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Orígenes permitidos para CORS (en dev se deja abierto)
BACKEND_CORS_ORIGINS=["*"]
```

---

##  Crear y activar el entorno virtual (Windows)

Desde la carpeta `backend_structure_only`:

### PowerShell / CMD

```bat
python -m venv .venv
.\.venv\Scripts\activate
```

### Git Bash

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Si todo va bien, verás algo como `(.venv)` o `()` al inicio de tu prompt.

---

## Instalar dependencias

Con el entorno virtual **activado**:

```bash
pip install -r requirements.txt
```

Además, instala el validador de emails que usa Pydantic:

```bash
pip install email-validator
```

> Si quieres dejarlo permanente, agrega `email-validator` a `requirements.txt`.

---

## Levantar el servidor

Con MySQL levantado y el venv activo:

```bash
uvicorn app.main:app --reload
```

Si todo está correcto deberías ver algo como:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
Base de datos inicializada correctamente.
```

---

## Probar la API

* Root (ping del backend):
  [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

* Documentación interactiva (Swagger):
  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

  Los endpoints de negocio estarán bajo el prefijo `/api/v1/...`
  (por ejemplo: `/api/v1/auth/login`, `/api/v1/farms`, `/api/v1/sensors`, etc.)

---

## Usuario administrador por defecto

En el script de inicialización (`app/db/init_db.py`) se crea automáticamente un usuario administrador si no existe:

* **Email:** `admin@agrodrone.com`
* **Contraseña:** `admin123`

Este usuario se genera al primer arranque de la aplicación durante el evento `startup`.

---

## Problemas comunes y soluciones rápidas

* **Error**:
  `ImportError: email-validator is not installed, run 'pip install pydantic[email]'`
  **Solución**:
  Ejecutar:

  ```bash
  pip install email-validator
  ```

* **Error**:
  `RuntimeError: 'cryptography' package is required for sha256_password or caching_sha2_password auth methods`
  **Soluciones posibles**:

  1. Instalar `cryptography`:

     ```bash
     pip install cryptography
     ```

  2. O cambiar el plugin del usuario en MySQL a `mysql_native_password` (ver sección 3).

* **Error**:
  `AttributeError: 'Settings' object has no attribute 'APP_NAME'`
  **Solución**:

  * Asegúrate de que `APP_NAME` está definido en `Settings` (`app/core/config.py`) **y** en el `.env`.

---

Con estos pasos cualquier miembro del equipo debería poder:

1. Clonar el repo
2. Configurar MySQL con Workbench
3. Levantar el entorno virtual
4. Ejecutar `uvicorn` y probar la API

sin tener que pelearse con MySQL ni dependencias extra.

```
```
