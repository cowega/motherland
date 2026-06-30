import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# Импортируем конфиг и модели бэкенда
from app.core.config import settings
from app.db import Base
# Импорт всех моделей, чтобы они были видны Alembic для autogenerate
from app.models import User, Location, Memory, MediaFile, Resident, PhotoTag

# Конфигурация Alembic
config = context.config

# Перезаписываем URL подключения из настроек Pydantic, которые берутся из .env
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные для автоматической генерации миграций
target_metadata = Base.metadata


def include_object(object, name, type_, reflected, compare_to):
    """Исключает любые таблицы, не принадлежащие нашему приложению (например, системные PostGIS)."""
    if type_ == "table":
        our_tables = {
            "users", "locations", "memories", "media_files", "residents", 
            "photo_tags", "alembic_version"
        }
        if name not in our_tables:
            return False
    return True


def run_migrations_offline() -> None:
    """Запуск миграций в режиме offline (вывод SQL-скрипта без подключения к БД)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """Вспомогательная функция для запуска миграций в транзакции."""
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Асинхронный запуск миграций для асинхронного движка SQLAlchemy."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Запуск миграций в режиме online (с подключением к БД)."""
    # Для асинхронного движка запускаем цикл событий
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
