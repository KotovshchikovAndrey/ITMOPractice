import uvicorn
from fastapi import FastAPI

from infrastructure import on_shutdown, on_startup
from infrastructure.api.v1.rest_routes import router as rest_router
from infrastructure.config.settings import settings

app = FastAPI(on_startup=[on_startup], on_shutdown=[on_shutdown])
app.include_router(rest_router)


if __name__ == "__main__":
    uvicorn.run(
        "index:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.is_dev,
    )
