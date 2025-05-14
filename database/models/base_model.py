from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
import threading


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)

    mutex = threading.Lock()

    @classmethod
    def create(cls, **kwargs) -> 'BaseModel' | None:
        try:
            pass
        except Exception:
            return None

    @classmethod
    def delete(cls, object_id: int) -> bool:
        try:
            return False
        except Exception:
            return False