import importlib

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("xdent-rag")


def _load_tools() -> None:
    """Import tool modules so FastMCP can register their decorators."""

    importlib.import_module("src.xdent_mcp.tools.theme")
    importlib.import_module("src.xdent_mcp.tools.transcript")


_load_tools()

app = mcp.streamable_http_app()
