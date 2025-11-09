# 🤖 AI Quiz Generator

This is a full-stack web application that generates challenging, AI-powered multiple-choice quizzes from any Wikipedia article.

The user provides a Wikipedia URL, and the application:
1.  **Scrapes** the article's content using the official Wikipedia API.
2.  **Generates** a 5-10 question quiz using the Google Gemini LLM (via LangChain).
3.  **Saves** the quiz and article data to a PostgreSQL or MySQL database.
4.  **Displays** the quiz in a clean, interactive React frontend where the user can take it.

## ## 🚀 Tech Stack

| Area | Technology |
| :--- | :--- |
| **Frontend** | React (Vite), Tailwind CSS, Axios |
| **Backend** | FastAPI (Python), SQLAlchemy |
| **Database** | PostgreSQL (Production) / MySQL (Local) |
| **AI** | Google Gemini (via `langchain-google-genai`) |
| **Scraping** | `wikipedia official url` |
| **Deployment** | Vercel (Frontend), Render (Backend) |

---

## ## ⚙️ Getting Started (Local Setup)

Follow these steps to set up and run the project on your local machine.

### ### Prerequisites

* [Node.js](https://nodejs.org/en) (v18+)
* [Python](https://www.python.org/downloads/) (v3.10+)
* A running PostgreSQL or MySQL database server.
* A Google Gemini API Key.

---

### ### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/ai-quiz-generator.git](https://github.com/your-username/ai-quiz-generator.git)
cd ai-quiz-generator
```

### ### 2. Backend Setup 🐍
#### 1. Navigate to the backend folder:

```bash
cd backend
```
#### 2. Create and activate a virtual environment:

```bash
py -m venv venv
.\venv\Scripts\activate
```
#### 3. Install Python packages:

```bash
pip install -r requirements.txt
```
#### 4. Create your environment file: Create a file named .env in the backend folder.
#### 5. Add your environment variables to the .env file.

```bash
GOOGLE_API_KEY="your_gemini_api_key_here"

# --- CHOOSE ONE DATABASE URL ---

# Example for PostgreSQL (Recommended for production)
# Make sure you have created a database named 'quiz_db'
DATABASE_URL="postgresql+psycopg2://your_user:your_pass@localhost:5432/quiz_db"

# Example for MySQL
# Make sure you have created a database named 'quiz_db'
DATABASE_URL="mysql+pymysql://root:my_p%40ssword@localhost:3306/quiz_db"
```
*Note: Remember to URL-encode special characters in your password (e.g., @ becomes %40).*

### ### 3. Frontend Setup ⚛️
#### 1. Navigate to the frontend folder (from the root):
```bash
cd frontend
```
#### 2. Install npm packages:
```bash
npm install
```
*This will also install Tailwind CSS and its dependencies.*
### 4. Run the Project
You must run both servers simultaneously in two separate terminals.

#### Terminal 1: Run the Backend (FastAPI)
```bash
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload
```
*(Backend will be running at http://localhost:8000)*

#### Terminal 2: Run the Frontend (React)
```bash
cd frontend
npm run dev
```
*(Frontend will be running at http://localhost:5173)*

Open http://localhost:5173 in your browser to use the app.

## 📡 API Endpoints

The backend provides the following endpoints:

### `POST /generate_quiz`
Generates a new quiz from a URL, saves it, and returns the full quiz object.

* **Body:**
    ```json
    {
      "url": "[https://en.wikipedia.org/wiki/Alan_Turing](https://en.wikipedia.org/wiki/Alan_Turing)"
    }
    ```

### `GET /history`
Gets a simplified list of all quizzes in the database.

### `GET /quiz/{quiz_id}`
Gets the full data for a single quiz by its ID.
