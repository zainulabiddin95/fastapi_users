import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from fastapi_users.config.app import app_config
from fastapi_users.config.log import logger


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

    return app


def main():
    app = create_app()

    print(app_config.database_ulr)

    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8080,
        proxy_headers=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
