import logging
import os
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)


class ConfigLoadError(Exception):
    pass


class Config:
    # Singleton pattern
    _instance: Optional["Config"] = None
    _initialized = False

    server_start_time = datetime.now(timezone.utc)

    PORT = 8000
    ENVIRONMENT = os.getenv("ENVIRONMENT", "pytest").lower()
    LOGGING_CONFIG_FILE: str = os.getenv(
        "LOG_CFG", "./datastore/logging_config_pytest.yaml"
    )

    DEFAULT_TIMEZONE = "UTC"
    LOCAL_TIMEZONE = os.getenv("LOCAL_TIMEZONE", DEFAULT_TIMEZONE)

    _sqlmodel_database_uri: Optional[str] = None
    _db_name: Optional[str] = None

    # The defaults / fallbacks are the Pytest flow, since Pytest doesn't run in the container but it
    # DOES run against the test DB/Redis containers.
    # TODO move the pytest config to conftest.py
    POSTGRES_USER_FILE: Optional[str] = None
    POSTGRES_USER_PASSWORD_FILE: Optional[str] = None
    TESTDB_USER_FILE_FALLBACK = "./secrets/datastore/test_postgres_user.txt"
    TESTDB_PASSWORD_FILE_FALLBACK = "./secrets/datastore/test_postgres_password.txt"
    DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "postgresql+asyncpg://")
    DBNAME = os.getenv("DATABASE_NAME", "chatterbox_testdb")
    DBSERVICE_NAME = os.getenv(
        "DB_SERVICE_NAME", "localhost"
    )  # "test-db" docker service name
    TEST_DBPORT_FALLBACK = "5433"
    DBPORT = os.getenv("DB_PORT", TEST_DBPORT_FALLBACK)

    # defaults are typical test-redis instance
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", "6380")
    REDIS_DB_INDEX = os.getenv("REDIS_DB", "0")

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def initialize(cls) -> None:
        if cls._initialized:
            return

        if cls.ENVIRONMENT in ["prod", "dev", "deploy"]:
            cls.POSTGRES_USER_FILE = os.getenv("DATABASE_USER_FILE")
            if cls.POSTGRES_USER_FILE is None:
                raise EnvironmentError("DATABASE_USER_FILE not in environment.")
            cls.POSTGRES_USER_PASSWORD_FILE = os.getenv("DATABASE_USER_PASSWORD_FILE")
            cls._db_name = os.getenv("DATABASE_NAME")
        elif cls.ENVIRONMENT in ["pytest", "test", "local"]:
            cls.POSTGRES_USER_FILE = os.getenv(
                "TEST_DATABASE_USER", cls.TESTDB_USER_FILE_FALLBACK
            )
            cls.POSTGRES_USER_PASSWORD_FILE = os.getenv(
                "TEST_DATABASE_PASSWORD_FILE", cls.TESTDB_PASSWORD_FILE_FALLBACK
            )
            cls._db_name = os.getenv("TEST_DB_NAME")
        else:
            raise ValueError(f"Invalid ENVIRONMENT set. {cls.ENVIRONMENT=}")

        cls._initialized = True

    @classmethod
    def _build_db_uri(cls) -> str:
        if not cls._initialized:
            cls.initialize()

        user: Optional[str] = None
        user_file = cls.POSTGRES_USER_FILE
        password: Optional[str] = None
        pw_file = cls.POSTGRES_USER_PASSWORD_FILE

        if pw_file is None:
            raise EnvironmentError(f"DB password file not set: {pw_file}")
        try:
            with open(pw_file, "r", encoding="utf8") as file:
                password = file.read().strip()
        except FileNotFoundError as e:
            raise EnvironmentError(f"DB password file missing: {pw_file}") from e
        if password is None or len(password) == 0:
            raise EnvironmentError(f"DB password file is empty: {pw_file}")

        if user_file is None:
            raise EnvironmentError(f"DB user file not set: {user_file}")
        try:
            with open(user_file, "r", encoding="utf8") as file:
                user = file.read().strip()
        except FileNotFoundError as e:
            raise EnvironmentError("DB username file missing.") from e
        if user is None or len(user) == 0:
            raise EnvironmentError("DB username file is empty.")

        # uri = f"mysql+aiomysql://user:{mysql_user_password}@db/lurkerbothunterdb"
        # uri = f"mysql+aiomysql://user:{password}@test-db:3307/lurkerbothunter-testdb"
        # uri = f"postgresql+asyncpg://user:password@postgres/chatterboxdb"
        prefix = cls.DATABASE_PREFIX
        credentials = f"{user}:{password}"
        port = cls.DBPORT
        if cls.DBPORT is not None:
            service_and_port = f"{cls.DBSERVICE_NAME}:{port}"
        else:
            service_and_port = f"{cls.DBSERVICE_NAME}:3306"
        uri = f"{prefix}{credentials}@{service_and_port}/{cls.DBNAME}"
        logger.debug(f"DB {uri=}")
        return uri

    @classmethod
    def get_db_uri(cls) -> str:
        if cls._sqlmodel_database_uri is None:
            cls._sqlmodel_database_uri = cls._build_db_uri()

        return cls._sqlmodel_database_uri

    @classmethod
    def get_redis_args(cls) -> dict[str, Any]:
        return {
            "host": Config.REDIS_HOST,
            "port": Config.REDIS_PORT,
            "db": Config.REDIS_DB_INDEX,
            "decode_responses": True,
        }
