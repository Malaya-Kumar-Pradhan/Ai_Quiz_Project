"""
main.py: The core FastAPI application file.

This file sets up the API endpoints for generating quizzes,
fetching quiz history, and retrieving specific quiz details.
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

# --- Import Our Custom Modules ---
from database import SessionLocal, Quiz, engine, Base
from scraper import scrape_wikipedia
from llm_quiz_generator import quiz_generation_chain
from models import QuizData as LLMQuizSchema  # Import Pydantic schema from models.py

# --- Pydantic Models for API Request/Response ---
from pydantic import BaseModel

class GenerateQuizRequest(BaseModel):
    """The JSON body expected for the /generate_quiz endpoint."""
    url: str

class QuizHistoryItem(BaseModel):
    """The simplified quiz object for the /history list."""
    id: int
    url: str
    title: str
    date_generated: datetime

    # This 'Config' allows Pydantic to read data from SQLAlchemy models
    class Config:
        orm_mode = True

class QuizDetailResponse(BaseModel):
    """The full quiz object for the /quiz/{quiz_id} endpoint."""
    id: int
    url: str
    title: str
    date_generated: datetime
    # The 'full_quiz_data' will be our deserialized JSON (LLMQuizSchema)
    full_quiz_data: LLMQuizSchema


# --- App Initialization ---

# Create all database tables (if they don't exist) on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Quiz Generator API",
    description="Generates quizzes from Wikipedia articles."
)

# --- CORS Middleware ---
# This allows your React frontend (e.g., from http://localhost:3000)
# to make requests to this API (e.g., on http://localhost:8000).

origins = [
    "http://localhost:3000",      # Default React app
    "http://localhost:5173",      # Default Vite app
    "https://ai-quiz-project.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# --- Database Session Dependency ---

def get_db():
    """
    FastAPI dependency to create and manage a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "AI Quiz Generator API is running!"}


@app.post("/generate_quiz", response_model=LLMQuizSchema)
async def generate_quiz(
    request: GenerateQuizRequest, 
    db: Session = Depends(get_db)
):
    """
    Endpoint 1: Generate a new quiz.
    1. Accepts a URL.
    2. Scrapes the content.
    3. Calls the LLM to generate a quiz.
    4. Saves the quiz to the database.
    5. Returns the generated quiz data.
    """
    
    # --- 1. Scrape Wikipedia ---
    print(f"Scraping {request.url}...")
    title, clean_text = scrape_wikipedia(request.url)
    
    if not clean_text or not title:
        raise HTTPException(status_code=404, detail="Could not scrape or find content at the provided URL.")
    
    # Limit text size to avoid huge API calls (e.g., first 15000 chars)
    if len(clean_text) > 15000:
        clean_text = clean_text[:15000]

    # --- 2. Call LLM Chain ---
    print("Scraping successful. Generating quiz...")
    try:
        # Use 'ainvoke' for async compatibility with FastAPI
        llm_output = await quiz_generation_chain.ainvoke({"article_text": clean_text})
    except Exception as e:
        print(f"LLM Error: {e}")
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {e}")
    
    print("Quiz generation successful. Saving to database...")
    
    # --- 3. Save to Database ---
    try:
        # Create the SQLAlchemy model instance
        db_quiz = Quiz(
            url=request.url,
            title=title,
            scraped_content=clean_text # Store the clean text
        )
        
        # Use the helper method from database.py to serialize the dict
        db_quiz.set_full_data(llm_output)
        
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
        
        print(f"Saved new quiz with ID: {db_quiz.id}")
        
        # --- 4. Return the generated quiz data ---
        # This 'llm_output' is a dict that matches our 'LLMQuizSchema'
        return llm_output
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Duplicate Entry Not Allowed")


@app.get("/history", response_model=List[QuizHistoryItem])
def get_history(db: Session = Depends(get_db)):
    """
    Endpoint 2: Get a list of all previously generated quizzes.
    Returns a simple list (id, url, title, date).
    """
    quizzes = db.query(Quiz).order_by(Quiz.date_generated.desc()).all()
    return quizzes


@app.get("/quiz/{quiz_id}", response_model=QuizDetailResponse)
def get_quiz_detail(quiz_id: int, db: Session = Depends(get_db)):
    """
    Endpoint 3: Get the full data for a single quiz.
    Fetches a specific quiz and deserializes its 'full_quiz_data'
    field back into a full JSON object.
    """
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # --- CRUCIAL: Deserialize ---
    # Use the helper method from our Quiz (SQLAlchemy) model
    deserialized_data = db_quiz.get_full_data()
    
    # Construct the response object
    response = QuizDetailResponse(
        id=db_quiz.id,
        url=db_quiz.url,
        title=db_quiz.title,
        date_generated=db_quiz.date_generated,
        full_quiz_data=deserialized_data # Pass the dict here
    )
    
    return response

# --- Uvicorn runner ---
if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
