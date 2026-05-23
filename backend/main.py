"""Application entry point dispatcher for API and MCP servers."""

import argparse
import asyncio
import contextlib


async def dispatch(server_type: str) -> None:
    """Start the requested server and keep it running until shutdown."""

    if server_type == "api":
        from src.api.setup import run_api_server

        await run_api_server()
        return

    if server_type == "mcp":
        from src.xdent_mcp.setup import run_mcp_server

        await run_mcp_server()
        return

    raise ValueError(f"Unsupported server type: {server_type}")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for selecting the server type."""

    parser = argparse.ArgumentParser(description="Start the API or MCP server.")
    parser.add_argument(
        "server_type",
        choices=("api", "mcp"),
        help="Which server to start.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(dispatch(args.server_type))
