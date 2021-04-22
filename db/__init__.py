from sqlalchemy.orm.session import Session
from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    return db
