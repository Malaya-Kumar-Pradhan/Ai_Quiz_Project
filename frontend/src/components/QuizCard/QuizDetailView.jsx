import React, { useState, useEffect } from 'react';
import { Loader2 } from 'lucide-react';
import * as api from '../../services/api';
import QuizDisplay from "../QuizDisplay.jsx";

function QuizDetailView({ quizId }) {
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!quizId) return;

    const fetchQuiz = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await api.getQuizById(quizId);
        setQuiz(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchQuiz();
  }, [quizId]);

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <Loader2 className="animate-spin text-blue-600" size={40} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-100 text-red-700 border border-red-300 rounded-lg">
        <strong>Error:</strong> {error}
      </div>
    );
  }

  if (!quiz) return null;

  return (
    <QuizDisplay title={quiz.title} quizData={quiz.full_quiz_data} />
  );
}

export default QuizDetailView;