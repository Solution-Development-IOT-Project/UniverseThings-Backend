
# UniverseThings-Backend (FastAPI + SQLAlchemy + MySQL)

Backend para la plataforma IoT agrícola **AgroDrone**, construido con  
**FastAPI, SQLAlchemy, Alembic y MySQL**. Incluye sensores, actuadores,
automatización por reglas, alertas, notificaciones, reportes y más.

---

## Tecnologías

- **FastAPI** (API REST)
- **SQLAlchemy 2.0** (ORM moderno)
- **MySQL** (Base de datos)
- **Alembic** (Migraciones)
- **Pydantic v2** (Validación de datos)
- **Passlib + bcrypt** (Hashing seguro)
- **JWT (python-jose)** (Autenticación)
- **PyTest** (Tests automáticos)

---

##  Instalación

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt

