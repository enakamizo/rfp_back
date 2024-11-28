from sqlalchemy import Column, Integer, String, Text
from database import Base

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), index=True)
    question_text = Column(Text, nullable=False)
    option1 = Column(Text, nullable=True)
    option2 = Column(Text, nullable=True)
    option3 = Column(Text, nullable=True)
    option4 = Column(Text, nullable=True)
    correct_option = Column(Integer, nullable=True)
    explanation = Column(Text, nullable=True)
