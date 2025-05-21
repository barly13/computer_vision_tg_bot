from sqlalchemy import Column, Integer, String, Float
from .base_model import BaseModel


class ExperimentReport(BaseModel):
    __tablename__ = 'experiment_report'

    image_path = Column(String, nullable=False)
    method1_result = Column(Float, nullable=False)
    method2_result = Column(Float, nullable=False)
    method3_result = Column(Float, nullable=False)