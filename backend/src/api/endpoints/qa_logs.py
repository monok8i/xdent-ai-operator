"""QA audit log export endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Query
from fastapi.responses import Response

from src.api.depends import QaLogExportServiceDependency


router = APIRouter(prefix="/qa-logs", tags=["qa-logs"])


@router.get("/export")
async def export_qa_logs(
    service: QaLogExportServiceDependency,
    limit: int = Query(default=1000, ge=1, le=10000),
    offset: int = Query(default=0, ge=0),
) -> Response:
    """Export QA audit logs as a CSV attachment."""

    filename, csv_content = await service.export_csv(limit=limit, offset=offset)
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return Response(
        content=csv_content,
        media_type="text/csv; charset=utf-8",
        headers=headers,
    )
