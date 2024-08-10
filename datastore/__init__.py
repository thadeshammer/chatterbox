import logging

from fastapi import Request, Response

from datastore.db import async_create_all_tables, async_session
from datastore.entities.models import ActionLog

from .datastore import create_app

logger = logging.getLogger(__name__)
app = create_app()

EXCLUDED_PATHS = ["/docs", "/openapi.json"]


@app.middleware("http")
async def log_request(request: Request, call_next):
    # Calls to the docs endpoint aren't necessary to log here
    if request.url.path in EXCLUDED_PATHS:
        return await call_next(request)

    query_params = str(request.url.query)
    parameters = query_params

    # If the request has a body (e.g., POST), read and log it, then replace it
    if request.method in ("POST", "PUT", "PATCH"):
        body = await request.body()
        parameters = body.decode("utf-8")

        # Repack the body into a new stream and attach it back to the request
        request._body = body  # pylint: disable=protected-access

    async with async_session() as session:
        action_log = ActionLog(endpoint=request.url.path, parameters=parameters)
        session.add(action_log)
        await session.commit()
        await session.refresh(action_log)

    log_id = action_log.id

    # call_next will swallow exceptions so we need to handle response codes here
    response: Response = await call_next(request)

    if not 200 <= response.status_code < 400:
        # Note that errors are logged in the API module prior to getting here.
        # Read the response body
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        # Process and log the body
        async with async_session() as session:
            action_log = await session.get(ActionLog, log_id)
            action_log.error_message = f"Error: {response.status_code}"
            action_log.error_message += f" - Detail: {response_body.decode()}"
            await session.commit()

        # Processing the body consumes it, so repack into a new response
        response = Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
    else:
        # A clean exit
        async with async_session() as session:
            action_log = await session.get(ActionLog, log_id)
            action_log.success = True
            await session.commit()

    return response
