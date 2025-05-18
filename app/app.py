import logging
from contextlib import asynccontextmanager

from api.v1.organisations import router as organisation_router
from config import settings
from database import sessionmanager
from fastapi import FastAPI


def init_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(organisation_router)

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        level=logging.INFO,
        format=settings.log_format,
        datefmt=settings.log_date_format,
        filename=settings.log_path,
        filemode="a",
    )

    sessionmanager.init(settings.postgres_url)
    logging.info("Database connection established.")

    yield

    if sessionmanager.engine:
        await sessionmanager.close()
        logging.info("Database connection closed.")


app = init_app()
