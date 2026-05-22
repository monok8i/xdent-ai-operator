from src.mcp.server import mcp


@mcp.tool()
def list_topics() -> list[dict[str, int | str]]:
    return [
        {"id": 1, "title": "calendar-scheduling-booking"},
        {"id": 2, "title": "certificate-authentication-setup"},
        {"id": 3, "title": "erecept"},
        {"id": 4, "title": "feature-requests-usability"},
        {"id": 5, "title": "how-to-product-navigation"},
        {"id": 6, "title": "integrations"},
        {"id": 7, "title": "printing-templates-documents"},
        {"id": 8, "title": "vzp"},
    ]
