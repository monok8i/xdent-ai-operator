"""API related exceptions."""

from fastapi import HTTPException, status


class NotImplementedError(HTTPException):
    def __init__(self, detail: str = "Feature is not implemented yet.") -> None:
        super().__init__(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=detail,
        )


class SearchError(HTTPException):
    def __init__(self, detail: str = "Failed to search documents.") -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )
