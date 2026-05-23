from src.api.schemas import ThemeResponse, Theme
from src.mcp.depends import get_repository
from src.mcp.server import mcp


@mcp.tool()
async def get_themes() -> dict[str, object]:
    """Return all available transcript themes."""

    async with get_repository() as repository:
        themes = await repository.get_themes()

    result = ThemeResponse(
        count=len(themes),
        themes=[Theme(id=theme.id, name=theme.name) for theme in themes],
    )

    return result.model_dump()
