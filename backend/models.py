"""
models.py

This file defines the Pydantic data validation models.
These models describe the exact JSON structure we expect
from the LLM's quiz generation output.
"""

from pydantic import BaseModel, Field
from typing import List,Literal

class Question(BaseModel):
    """A Pydantic model for a single multiple-choice question."""
    
    question_id: str = Field(description="A unique identifier for the question, e.g., 'q1', 'q2'.")
    text: str = Field(description="The full text of the question.")
    options: List[str] = Field(description="A list of 4 potential answers.")
    answer: str = Field(description="The one correct answer, which must match one of the options exactly.")
    explanation: str = Field(description="A brief (1-2 sentence) explanation for why the answer is correct.")
    difficulty: Literal['easy', 'medium', 'hard'] = Field(description="The difficulty level of the question.")

class QuizData(BaseModel):
    """
    The main Pydantic model representing the entire quiz structure.
    This is what the LLM will be forced to output.
    """
    id: int = Field(description="Give unique id to each quiz for e.g 1, 2,...")
    title : str = Field(description="Give the title for the quiz like 'Python Programming Language'.")
    summary: str = Field(description="Provide a summary of the topic like a small paragraph")
    key_entities: List[str] = Field(description="A list of 3-5 key topics, names, or entities from the provided text.")
    organizations:List[str] = Field(description="A list of 2-3 organization from the provided text.")
    locations: List[str] = Field(description="Provide the location from where the information is being released")
    sections: List[str] = Field(description="A list of 2-3 sections from the provided text.")
    suggested_topics: List[str] = Field(
        description="A list of 3-5 related Wikipedia topics or concepts for further reading."
    )
    
    quiz: List[Question] = Field(
        description="A list of 5-10 multiple-choice questions based on the text."
    )