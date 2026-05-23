"""Application setup helpers for building the FastAPI server."""

import asyncio
import signal

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import router as api_router
from src.api.events.lifespan import lifespan
from src.core.config._global import config
from src.utils.logging.setup import setup_logging, stop_logging


def create_fastapi() -> FastAPI:
    """Create the FastAPI application and register shared state and routers.

    Returns:
        Configured FastAPI application instance.
    """

    app = FastAPI(title="What Now API", lifespan=lifespan)
    app.state.project_config = config
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.api.ALLOW_ORIGINS,
        allow_credentials=config.api.ALLOW_CREDENTIALS,
        allow_methods=config.api.ALLOW_METHODS,
        allow_headers=config.api.ALLOW_HEADERS,
    )

    app.include_router(api_router)

    return app


def create_api_server() -> uvicorn.Server:
    """Build the Uvicorn server wrapper around the FastAPI application.

    Returns:
        Configured Uvicorn server instance.
    """

    app = create_fastapi()

    return uvicorn.Server(
        uvicorn.Config(
            app=app,
            host=config.api.API_HOST,
            port=config.api.API_PORT,
            log_config=None,
        )
    )


async def run_api_server() -> None:
    """Start the FastAPI server and keep it running until shutdown."""

    logger = setup_logging()
    server = create_api_server()
    server_task = asyncio.create_task(server.serve())

    loop = asyncio.get_running_loop()

    def shutdown() -> None:
        """Request a graceful server shutdown from the signal handler."""

        logger.info("Shutdown signal received. Stopping the server...")
        server.should_exit = True

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, shutdown)

    try:
        await server_task
    except asyncio.CancelledError:
        logger.info("Server task was cancelled.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info("API has been stopped.")
        stop_logging()
