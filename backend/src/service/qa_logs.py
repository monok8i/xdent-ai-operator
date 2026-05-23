"""QA audit log export service."""

from __future__ import annotations

import csv
import io
from datetime import UTC

from src.infra.db.question_answer_log_repository import QuestionAnswerLogRepository


class QaLogExportService:
    """Build CSV exports for QA audit logs."""

    def __init__(self, repository: QuestionAnswerLogRepository) -> None:
        self._repository = repository

    async def export_csv(self, *, limit: int, offset: int) -> tuple[str, str]:
        """Return a CSV filename and payload for the requested slice."""

        rows = await self._repository.list_for_export(limit=limit, offset=offset)

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["id", "created_at", "prompt", "answer"])

        for row in rows:
            created_at = row.created_at.astimezone(UTC).isoformat()
            writer.writerow([row.id, created_at, row.prompt, row.answer])

        filename = f"qa-logs-{len(rows)}-items.csv"
        return filename, buffer.getvalue()
