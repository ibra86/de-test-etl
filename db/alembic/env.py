import os
import sys
from pathlib import Path
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# --- .env support (optional) ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# --- Alembic config ---
config = context.config

db_url = os.getenv("DATABASE_URL") or config.get_main_option("sqlalchemy.url", "")
if not db_url:
    raise RuntimeError(
        "No DATABASE_URL and sqlalchemy.url not set. "
        "Set DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname"
    )
config.set_main_option("sqlalchemy.url", db_url)

# --- Logging ---
if config.config_file_name:
    fileConfig(config.config_file_name)

# --- Make project importable and load SQLAlchemy metadata ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]   # repo root (../)
sys.path.insert(0, str(PROJECT_ROOT))  # noqa: E402

from db.sa_models import Base  # noqa: E402
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        compare_type=True,              # detect type changes
        compare_server_default=True,    # detect default changes
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # version_table_schema="public",   # uncomment if you manage schemas
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            # version_table_schema="public",
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
