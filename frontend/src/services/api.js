import axios from 'axios';

// Create an Axios instance configured to talk to your backend
const apiClient = axios.create({
  baseURL: 'https://ai-quiz-project-ix11.onrender.com', // Your FastAPI server address
});

/**
 * Sends a URL to the backend to generate a new quiz.
 * @param {string} url The Wikipedia URL.
 * @returns {Promise<object>} The generated quiz data.
 */
export const generateQuiz = async (url) => {
  try {
    const response = await apiClient.post('/generate_quiz', { url });
    return response.data;
  } catch (error) {
    console.error("Error generating quiz:", error);
    throw new Error(error.response?.data?.detail || "Failed to generate quiz");
  }
};

/**
 * Fetches the list of all previously generated quizzes.
 * @returns {Promise<Array>} A list of quiz history items.
 */
export const getHistory = async () => {
  try {
    const response = await apiClient.get('/history');
    return response.data;
  } catch (error) {
    console.error("Error fetching history:", error);
    throw new Error(error.response?.data?.detail || "Failed to fetch history");
  }
};

/**
 * Fetches the full details for a single quiz by its ID.
 * @param {number} quizId The ID of the quiz.
 *IS * @returns {Promise<object>} The full quiz detail object.
 */
export const getQuizById = async (quizId) => {
  try {
    const response = await apiClient.get(`/quiz/${quizId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching quiz detail:", error);
    throw new Error(error.response?.data?.detail || "Failed to fetch quiz");
  }
};
