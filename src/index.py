import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from domain.exceptions.api_exception import ApiException
from infrastructure import on_shutdown, on_startup
from infrastructure.api.v1.auth_routes import router as auth_router
from infrastructure.api.v1.city_point_routes import router as city_point_router
from infrastructure.api.v1.user_routes import router as user_router
from infrastructure.config.settings import settings
from infrastructure.helpers.mappers import HttpExceptionStatusMapper

app = FastAPI(on_startup=[on_startup], on_shutdown=[on_shutdown])

app.include_router(city_point_router, prefix=settings.api_prefix)
app.include_router(user_router, prefix=settings.api_prefix)
app.include_router(auth_router, prefix=settings.api_prefix)


@app.exception_handler(RequestValidationError)
async def handle_validation_exception(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": exc.errors(),
        },
    )


@app.exception_handler(ApiException)
def handle_api_exception(request: Request, exc: ApiException):
    mapper = HttpExceptionStatusMapper(exception=exc)
    status_code = mapper.do_mapping()

    return JSONResponse(
        status_code=status_code,
        content={
            "status_code": status_code,
            "message": exc.message,
        },
    )


@app.exception_handler(Exception)
def handle_internal_server_error(request: Request, exc: ApiException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Внутренняя ошибка сервера!",
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        "index:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.is_dev,
    )
