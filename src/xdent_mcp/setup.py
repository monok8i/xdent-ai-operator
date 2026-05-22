"""Application setup helpers for building the MCP server."""

import asyncio
import signal

import uvicorn

from src.core.config._global import config
from src.utils.logging.setup import setup_logging, stop_logging
from src.xdent_mcp.server import app


def create_mcp_server() -> uvicorn.Server:
    """Build the Uvicorn server wrapper around the MCP ASGI app.

    Returns:
        Configured Uvicorn server instance.
    """

    return uvicorn.Server(
        uvicorn.Config(
            app=app,
            host=config.mcp.MCP_HOST,
            port=config.mcp.MCP_PORT,
            log_config=None,
        )
    )


async def run_mcp_server() -> None:
    """Start the MCP server and keep it running until shutdown."""

    logger = setup_logging()
    server = create_mcp_server()
    server_task = asyncio.create_task(server.serve())

    loop = asyncio.get_running_loop()

    def shutdown() -> None:
        """Request a graceful server shutdown from the signal handler."""

        logger.info("Shutdown signal received. Stopping the MCP server...")
        server.should_exit = True

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, shutdown)

    try:
        await server_task
    except asyncio.CancelledError:
        logger.info("MCP server task was cancelled.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info("MCP has been stopped.")
        stop_logging()
