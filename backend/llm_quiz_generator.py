"""
llm_quiz_generator.py

This file contains the logic for generating a quiz using an LLM (Gemini)
and enforcing a strict JSON output using Pydantic.
"""

import os
import json
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models import QuizData  # <-- Import our Pydantic schema

# --- 1. Setup ---

# Load environment variables from that specific path
load_dotenv()
# Load environment variables (for GEMINI_API_KEY)
api_key = os.getenv("GEMINI_API_KEY")

if not os.getenv("GEMINI_API_KEY"):
    raise EnvironmentError("GEMINI_API_KEY not found in .env file")

# --- 2. Initialize the Model ---
# We use gemini-2.5-flash for speed and cost-effectiveness
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=api_key, temperature=0.3)

# --- 3. Setup Parser ---
# Create an instance of the JsonOutputParser, passing our Pydantic model
parser = JsonOutputParser(pydantic_object=QuizData)

# --- 4. Define the Prompt Template ---
# This is a detailed prompt that instructs the LLM
prompt_template = """
You are an expert quiz creator. Your task is to generate a challenging,
multiple-choice quiz based on the provided article text.

The quiz should test key concepts, facts, and entities from the text.
You must generate 5-10 questions.

For each question, you must provide:
1.  The question text.
2.  Four multiple-choice options.
3.  The single correct answer.
4.  A **short explanation** for why that answer is correct.
5.  A **difficulty rating** ('easy', 'medium', or 'hard').

You must also provide a list of 3-5 **suggested related topics** for further reading.

Here is the article text:
---
{article_text}
---

Now, generate the quiz. You must follow this exact JSON format.
{format_instructions}
"""

# Create the LangChain PromptTemplate object
prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["article_text"],
    # We pass the parser's instructions as a partial variable
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# --- 5. Create the Chain ---
# We chain the components together using LangChain Expression Language (LCEL)
# The chain will:
# 1. Take the "article_text"
# 2. Format the prompt
# 3. Send the prompt to the LLM
# 4. Take the LLM's string output and pass it to the parser
# 5. The parser returns a Python dictionary (from the parsed JSON)
quiz_generation_chain = prompt | llm | parser

# --- Example Usage ---
if __name__ == "__main__":
    
    print("Testing the quiz generation chain...")
    
    # A short, simple text for testing
    test_article = """
    Python is a high-level, general-purpose programming language.
    Its design philosophy emphasizes code readability with the use of 
    significant indentation. It was created by Guido van Rossum and 
    first released in 1991. Python is dynamically typed and 
    garbage-collected. It supports multiple programming paradigms, 
    including structured, object-oriented and functional programming.
    """
    
    try:
        # Run the chain
        # The .invoke() method passes the input to the chain
        output = quiz_generation_chain.invoke({"article_text": test_article})
        
        print("\nChain run successful!")
        print("\n--- Generated Quiz (as Python dict) ---")
        # Pretty-print the dictionary
        print(json.dumps(output, indent=2))

    except Exception as e:
        print(f"\nAn error occurred:")
        print(e)