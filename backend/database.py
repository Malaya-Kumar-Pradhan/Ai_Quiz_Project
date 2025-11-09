"""
This file defines the database connection (engine),
the declarative base, and the data models for the quiz app.
"""

import datetime
import json
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# --- 1. Define Database Connection ---
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- 2. Define Base Class ---

# Create a declarative base class for your models to inherit from
class Base(DeclarativeBase):
    pass

# --- 3. Define the Quiz Model ---

class Quiz(Base):
    """
    Model representing a generated quiz.
    The full quiz data is serialized as JSON in the 'full_quiz_data' field.
    """
    
    # The name of the table in the database
    __tablename__ = "quiz_history"

    # Define the fields (columns)
    id = Column(Integer, primary_key=True)
    url = Column(String(500), nullable=False, unique=True)
    title = Column(String(250), default="Untitled Quiz")
    date_generated = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Bonus field for the raw scraped text
    scraped_content = Column(Text, nullable=True)
    
    # CRUCIAL: This field stores the complex quiz data as a simple string
    full_quiz_data = Column(Text, nullable=False)

    def __repr__(self):
        # A helpful representation for printing and debugging
        return f"<Quiz(id={self.id}, url='{self.url[:50]}...')>"

    # --- Helper methods for the JSON field ---

    def set_full_data(self, data_dict: dict):
        """
        Takes a Python dictionary and serializes it
        (converts to a JSON string) to store in the database.
        """
        self.full_quiz_data = json.dumps(data_dict)
    
    def get_full_data(self) -> dict:
        """
        Deserializes the JSON string from the database
        back into a Python dictionary.
        """
        if not self.full_quiz_data:
            return {}
        try:
            return json.loads(self.full_quiz_data)
        except json.JSONDecodeError:
            # Handle cases where data might be corrupted
            return {"error": "Invalid JSON data in database"}

# --- Helper function to create tables ---

def create_db_and_tables():
    """
    Finds all classes that inherit from 'Base' and creates
    the corresponding tables in the database.
    """
    print("Creating database and tables...")
    Base.metadata.create_all(bind=engine)
    print(f"Database 'quiz_history.db' and table '{Quiz.__tablename__}' are ready.")

# This allows us to run `python database.py` from my terminal
# to create the database file and tables before running my main app.
if __name__ == "__main__":
    create_db_and_tables()
