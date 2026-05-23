# XDent RAG system

## MCP tools

The project exposes two MCP tools through `src/mcp/server.py`:

- `search_transcripts`: embeds the user's prompt, filters by `theme_id`, and returns ranked transcript matches.
- `get_themes`: returns the full list of transcript themes.

Both tools reuse the same repository and dependency wiring as the FastAPI application, so they read from the same database and embedding client.

## AI answer endpoint

The backend also exposes a transcript-backed AI answer endpoint:

- `POST /api/v1/answer` accepts only `prompt` and returns only `message`.

The endpoint first selects the best transcript theme, then searches transcripts inside that theme, and finally asks the AI model to generate the final response from the prompt plus retrieved transcript excerpts.

Required AI settings:

- `AI_API_KEY` or `OPENAI_API_KEY`
- `AI_MODEL` or `OPENAI_MODEL`
- `AI_BASE_URL` or `OPENAI_BASE_URL`

## Run FastAPI and MCP together

Use two terminals so each process can run independently:

```bash
uv run uvicorn main:app --reload
```

```bash
uv run python -m src.mcp.server
```

The first command starts the HTTP API. The second command starts the MCP server over stdio, which is the usual transport for local MCP clients.

## Docker Compose

The repository also ships with separate Docker services for the API and MCP server:

- `xdent-backend` runs FastAPI.
- `xdent-mcp` runs the MCP server on port `8001` using `streamable-http`.

Bring both up with:

```bash
docker compose up --build xdent-backend xdent-mcp xdent-backend-db
```