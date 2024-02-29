import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from fastapi_users.config.log import logger
from fastapi_users.router.auth import auth_router


def create_app() -> FastAPI:
    app = FastAPI()

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        logger.error(f"Request validation error: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors(), "body": exc.body},
        )

    app.include_router(auth_router)

    return app


def main():
    app = create_app()

    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8080,
        proxy_headers=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
