from sqlalchemy import Column, Integer, String, DateTime, Boolean
from .base_model import BaseModel


class ExperimentReport(BaseModel):
    __tablename__ = 'experiment_report'

    id = Column(Integer, primary_key=True)
    image_path = Column(String, nullable=True)
    generation_params = Column(String, nullable=True)
    is_generated = Column(Boolean, nullable=False, default=False)

    date = Column(DateTime, nullable=False)

    opencv_result = Column(Integer, nullable=False)
    ml_result = Column(Integer, nullable=False)
    cnn_result = Column(Integer, nullable=False)