from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
import os

# Adiciona o diretório raiz ao path do Python
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Importa todas as models
from Models.auth_models import Base as AuthBase
from Models.clients_models import Base as ClientsBase
from Models.products_models import Base as ProductsBase
from Models.categories_models import Base as CategoriesBase
from Models.sections_models import Base as SectionsBase
from Models.orders_models import Base as OrdersBase

# Congiguração do objeto config
config = context.config

# Interpretar o arquivo de configuração para logging em Python
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Adiciona todas as metadata das models
target_metadata = [AuthBase.metadata, ClientsBase.metadata, ProductsBase.metadata, 
                  CategoriesBase.metadata, SectionsBase.metadata, OrdersBase.metadata]

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


