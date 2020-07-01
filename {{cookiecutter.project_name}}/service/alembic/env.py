from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

from conf import PG_URI
from database import Base

config = context.config
config.set_main_option('sqlalchemy.url', PG_URI)

fileConfig(config.config_file_name)  # setting up loggers

target_metadata = Base.metadata


def make_exclude_tables(config_):
    tables_ = config_.get('tables', '')
    return tables_.split(',')


exclude_tables = make_exclude_tables(config.get_section('alembic:exclude'))


def include_object(object_, name, type_, reflected, compare_to):
    return not (type_ == 'table' and name in exclude_tables)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=PG_URI,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
        include_object=include_object,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(PG_URI)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
