"""Error handling middleware for FastAPI."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


def setup_error_handlers(app: FastAPI) -> None:
    """Setup global error handlers for FastAPI application.

    Args:
        app: FastAPI application instance.
    """

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
        """Handle ValueError exceptions.

        Args:
            request: Incoming request.
            exc: ValueError exception.

        Returns:
            JSON error response.
        """
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "validation_error",
                "message": str(exc),
                "path": str(request.url.path),
            },
        )

    @app.exception_handler(Exception)
    async def general_error_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle general exceptions.

        Args:
            request: Incoming request.
            exc: Exception.

        Returns:
            JSON error response.
        """
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "internal_server_error",
                "message": "An unexpected error occurred",
                "path": str(request.url.path),
            },
        )
