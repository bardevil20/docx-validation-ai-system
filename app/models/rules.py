from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Rules(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    
    analysis_id = Column(Integer, ForeignKey("analysis_jobs.id"), nullable=False)
    
    rule_text = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    quote = Column(Text, nullable=True)

    # relationship to the analysis table, using the analysis_id column
    analysis = relationship("Analysis", back_populates="rules")