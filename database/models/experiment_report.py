from sqlalchemy import Column, Integer, String, Float, DateTime
from .base_model import BaseModel


class ExperimentReport(BaseModel):
    __tablename__ = 'experiment_report'

    image_path = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    method1_result = Column(Integer, nullable=False)
    method2_result = Column(Integer, nullable=False)
    method3_result = Column(Integer, nullable=False)