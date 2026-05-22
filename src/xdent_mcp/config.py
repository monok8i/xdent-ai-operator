"""MCP server configuration settings."""

from src.core.config.env import BaseEnvConfig


class Config(BaseEnvConfig):
    """Host and port used by the MCP server.

    Attributes:
        MCP_HOST: Host interface the MCP server listens on.
        MCP_PORT: TCP port the MCP server listens on.
    """

    MCP_HOST: str = "0.0.0.0"
    MCP_PORT: int = 8001
