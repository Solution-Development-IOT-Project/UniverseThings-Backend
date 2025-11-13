from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import os
import sys

# -----------------------------------------
# Añadir el proyecto al PYTHONPATH
# -----------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))

# Importar settings y Base de modelos
from app.core.config import settings
from app.db.base import Base  # Aquí están TODOS tus modelos importados


# -----------------------------------------
# Configuración Alembic
# -----------------------------------------
config = context.config

# Interpretar logging config del alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Definir MetaData target
target_metadata = Base.metadata


# -----------------------------------------
# Configurar la URL desde tus settings
# -----------------------------------------
def get_url():
    return settings.SQLALCHEMY_DATABASE_URL


# -----------------------------------------
# Modo OFFLINE → genera SQL sin ejecutar
# -----------------------------------------
def run_migrations_offline():
    url = get_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # detectar cambios en tipos
    )

    with context.begin_transaction():
        context.run_migrations()


# -----------------------------------------
# Modo ONLINE → migraciones sobre la BD real
# -----------------------------------------
def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)

    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,       # detectar cambios en tipos
            compare_server_default=True,
            compare_nullable=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# -----------------------------------------
# PUNTO DE ENTRADA
# -----------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
