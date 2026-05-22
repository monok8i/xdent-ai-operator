from typing import Any
from src.mcp.server import mcp
from src.api.depends import TranscriptRepositoryDependency
from src.api.schemas import ThemeResponse, Theme


@mcp.tool()
async def get_themes(
    repository: TranscriptRepositoryDependency,
) -> dict[str, Any]:
    """Return all available transcript themes."""

    themes = await repository.get_themes()
    count = len(themes)

    result = ThemeResponse(
        count=count, themes=[Theme(id=theme.id, name=theme.name) for theme in themes]
    )

    return result.model_dump()
