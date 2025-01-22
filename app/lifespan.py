from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from app.database.db import init_db

@asynccontextmanager
async def lifespan(app:FastAPI):
    """ app lifespan
     
        You can do more like initate db table, migration , others
    """
    logging.log(1,"initalizing database")
    await init_db()
    yield




