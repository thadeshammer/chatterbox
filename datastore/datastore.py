import logging
import os
import ssl
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from datastore.entities.models import (  # pylint: disable=unused-import
    Board,
    Category,
    Comment,
    CommentVote,
    Event,
    EventVote,
    Post,
    PostVote,
    User,
    UserProfile,
)

from .config import Config
from .db import async_create_all_tables
from .utils import setup_logging

CERT_FILE_PATH = os.getenv("CERT_FILE_PATH")
KEY_FILE_PATH = os.getenv("KEY_FILE_PATH")
CERT_PASSKEY = os.getenv("CERT_PASSKEY")

# Logger setup outside of create_app
setup_logging(Config.LOGGING_CONFIG_FILE)

# "Using selector: EpollSelector" spam
logging.getLogger("asyncio").setLevel(logging.WARNING)
# Set to DEBUG to figure out the at-times misleading greenlet spawn error.
# See /tests/datastore/model_sanity/test_greenlet_red_herring to do this.
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to debug level to capture detailed logs
logger.info("Logger is ready.")


@asynccontextmanager
async def lifespan(
    fastapi_app: FastAPI,  # type: ignore  pylint:disable=unused-argument
) -> AsyncGenerator[None, None]:
    # Startup events
    logger.info("DATASTORE START")
    Config.initialize()
    await async_create_all_tables()

    yield  # this allows the server to run

    # Shutdown event
    # Add any necessary cleanup code here
    logger.info("DATASTORE STOP")


def create_app() -> FastAPI:
    fastapi_app = FastAPI(lifespan=lifespan)
    fastapi_app.debug = False

    # TODO create and setup basic router
    # fastapi_app.include_router(router)

    return fastapi_app


if __name__ == "__main__":
    if CERT_FILE_PATH is None:
        raise EnvironmentError("CERT_FILE_PATH environment variable is not set.")
    if os.path.isfile(CERT_FILE_PATH) is False:
        raise FileNotFoundError(f"Cert file not at {CERT_FILE_PATH=}")

    if KEY_FILE_PATH is None:
        raise EnvironmentError("KEY_FILE_PATH environment variable is not set.")
    if os.path.isfile(KEY_FILE_PATH) is False:
        raise FileNotFoundError(f"Key file not at {KEY_FILE_PATH=}")

    if CERT_PASSKEY is None:
        raise EnvironmentError("CERT_PASSKEY environment variable is not set.")

    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(
            certfile=CERT_FILE_PATH,
            keyfile=KEY_FILE_PATH,
            password=CERT_PASSKEY,
        )
    except FileNotFoundError as e:
        print(f"File not found. {str(e)}")
        raise
