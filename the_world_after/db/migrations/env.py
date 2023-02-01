import asyncio
import logging

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine

from the_world_after.db.db import Base
from the_world_after.db.models.player import Player  # noqa
from the_world_after.settings import settings
from the_world_after.utils.logs import init_logger

init_logger(settings.LOG_CONFIG)

logger = logging.getLogger("alembic")

# this is the Alembic Config object, which provides access
# to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", str(settings.DB_DSN))

# Interpret the config file for Python logging.
# This line sets up loggers basically.

# add your model's MetaData object here for 'autogenerate' support
target_metadata = (Base.metadata,)


# other values from the config, defined by the needs of env.py, can be acquir:
# my_important_option = config.get_main_option("my_important_option")


def include_name(name, type_, parent_names):
    if type_ == "table":
        return any(name in metadata.tables for metadata in target_metadata)
    else:
        return True


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_name=include_name,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


try:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())
except Exception:
    logger.exception("Migrations fault")
