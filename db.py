import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Define database file path — os.getcwd() is reliable on both local & Streamlit Cloud
DB_PATH = os.path.join(os.getcwd(), 'data', 'evaluations.db')

# Create engine
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)

# Define Base
Base = declarative_base()

class Evaluation(Base):
    __tablename__ = 'evaluations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False) # 'writing' or 'speaking'
    input_text = Column(Text, nullable=True) # User's original text (writing)
    transcript = Column(Text, nullable=True) # STT result (speaking)
    audio_path = Column(String(255), nullable=True) # Path to saved audio (speaking)
    
    # Scores (0-100 or 1-10, we'll use 0-100)
    grammar_score = Column(Float, nullable=True)
    vocabulary_score = Column(Float, nullable=True)
    coherence_score = Column(Float, nullable=True)
    fluency_score = Column(Float, nullable=True) # mostly for speaking
    overall_score = Column(Float, nullable=True)
    
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(engine)

# Create Session class
SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()
