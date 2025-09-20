from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from importlib import import_module  # Import importlib for dynamic imports

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here
# for 'autogenerate' support
# This ensures that all models are included for migrations
target_metadata = None  # Will be assigned later

def import_models():
    """Dynamically import models to avoid circular imports."""
    global target_metadata
    import_module('api.models.trip')  # Import Trip model
    import_module('api.models.companion_request')  # Import CompanionRequest model
    import_module('auth.models')  # Import User model

    # Now that models are imported, we can access the metadata
    from api.models.trip import Trip
    from api.models.companion_request import CompanionRequest
    from auth.models import User
    from database import BaseModel  # BaseModel will contain the metadata
    target_metadata = BaseModel.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        {'sqlalchemy.url': DATABASE_URL},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Import models before running migrations
import_models()

# Run migrations based on whether it's offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
