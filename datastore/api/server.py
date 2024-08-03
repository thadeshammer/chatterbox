import logging
from datetime import datetime, timezone

import pytz
from fastapi import APIRouter

from datastore.config import Config

server_routes = APIRouter()
logger = logging.getLogger(__name__)


@server_routes.get("/healthcheck/")
async def healthcheck():
    current_time = datetime.now(timezone.utc)

    try:
        local_timezone = pytz.timezone(Config.LOCAL_TIMEZONE)
        server_start_local = Config.server_start_time.astimezone(local_timezone)
        current_time_local = current_time.astimezone(local_timezone)
    except pytz.UnknownTimeZoneError:
        logger.error(
            f"Check config: {Config.LOCAL_TIMEZONE} is unknown. Defaulting to {Config.DEFAULT_TIMEZONE}"
        )
        local_timezone = pytz.timezone(Config.DEFAULT_TIMEZONE)
        server_start_local = "Error: check config. Use IANA db timezone code."
        current_time_local = "Error: check config. Use IANA db timezone code."

    uptime = current_time - Config.server_start_time
    return {
        "status": "ok",
        "server_start_time": f"{Config.server_start_time.isoformat()} ({server_start_local})",
        "current_time": f"{current_time.isoformat()} ({current_time_local})",
        "uptime": str(uptime),
    }
