import React, { useState } from 'react';
import { Loader2 } from 'lucide-react';
import * as api from '../services/api';
import QuizDisplay from "../components/QuizDisplay.jsx";

function GenerateQuizTab() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [quizResult, setQuizResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Simple URL Validation
    if (!url || !url.includes('wikipedia.org')) {
      setError('Please enter a valid Wikipedia URL.');
      return;
    }

    setError(null);
    setQuizResult(null);
    setLoading(true);

    try {
      const data = await api.generateQuiz(url);
      setQuizResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
      setUrl('')
    }
  };

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="flex space-x-3">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter a Wikipedia URL..."
          className="flex-grow p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
          disabled={loading}
        />
        <button
          type="submit"
          className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
          disabled={loading}
        >
          {loading ? (
            <Loader2 className="animate-spin" />
          ) : (
            'Generate Quiz'
          )}
        </button>
      </form>

      {error && (
        <div className="p-4 bg-red-100 text-red-700 border border-red-300 rounded-lg">
          <strong>Error:</strong> {error}
        </div>
      )}

      {quizResult && (
        <div className="mt-8">
          <h2 className="text-2xl font-bold mb-4">Generated Quiz</h2>
          <QuizDisplay quizData={quizResult} />
        </div>
      )}
    </div>
  );
}

export default GenerateQuizTab;