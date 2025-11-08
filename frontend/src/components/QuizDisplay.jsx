import React, { useState } from 'react';

function QuizDisplay({ quizData }) {
  if (!quizData) return null;

  const [selections, setSelections] = useState({});
  const totalQuestions = quizData.quiz.length;

  const handleOptionClick = (questionId, option) => {
    if (selections[questionId]) {
      return;
    }
    setSelections((prevSelections) => ({
      ...prevSelections,
      [questionId]: option,
    }));
  };

  const getButtonClass = (question, option) => {
    const userSelection = selections[question.question_id];
    const isCorrect = question.answer === option;
    const isSelected = userSelection === option;
    let baseStyle = 'p-2 rounded w-full text-left mb-2 transition-colors';

    if (!userSelection) {
      return `${baseStyle} bg-gray-200 hover:bg-gray-300`;
    }
    if (isSelected) {
      return isCorrect
        ? `${baseStyle} bg-green-500 text-white`
        : `${baseStyle} bg-red-500 text-white`;
    }
    if (isCorrect) {
      return `${baseStyle} bg-green-500 text-white opacity-70`;
    }
    return `${baseStyle} bg-gray-200 opacity-60 cursor-not-allowed`;
  };

  // --- Logic for Final Results ---
  const isQuizComplete = Object.keys(selections).length === totalQuestions;
  
  // Calculate wrong answers only when the quiz is complete
  let wrongAnswerCount = 0;
  if (isQuizComplete) {
    quizData.quiz.forEach(q => {
      const userSelection = selections[q.question_id];
      if (userSelection && userSelection !== q.answer) {
        wrongAnswerCount++;
      }
    });
  }
  // --- End Final Results Logic ---

  return (
    <div className="space-y-6">
      {/* Key Entities */}
      <div>
        <h3 className="text-xl font-semibold text-gray-700 mb-3">Key Entities</h3>
        <div className="flex flex-wrap gap-2">
          {quizData.key_entities.map((entity, index) => (
            <span
              key={index}
              className="bg-gray-200 text-gray-800 px-3 py-1 rounded-full text-sm font-medium gap-5"
            >
              {entity}
            </span>
          ))}
        </div>
      </div>

      {/* Questions */}
      <div className="space-y-5">
        <h3 className="text-xl font-semibold text-gray-700 mb-3">Questions</h3>
        <ul className="space-y-4">
          {quizData.quiz.map((q) => (
            <li key={q.question_id} className="bg-white p-4 rounded-lg shadow-sm">
              <p className="font-medium text-gray-800 mb-3">{q.text}</p>
              <div className="flex flex-col">
                {q.options.map((each) => (
                  <button
                    type="button"
                    key={each}
                    onClick={() => handleOptionClick(q.question_id, each)}
                    disabled={!!selections[q.question_id]}
                    className={getButtonClass(q, each)}
                  >
                    {each}
                  </button>
                ))}
              </div>

              {/* SIMPLIFIED: Show only explanation on a per-question basis */}
              {(() => {
                const userSelection = selections[q.question_id];
                if (!userSelection) return null; // No selection yet

                const isCorrect = userSelection === q.answer;

                return (
                  <div
                    className={`mt-3 p-3 rounded border ${
                      isCorrect
                        ? 'bg-green-50 border-green-200'
                        : 'bg-red-50 border-red-200'
                    }`}
                  >
                    <p
                      className={`text-sm font-semibold ${
                        isCorrect ? 'text-green-800' : 'text-red-800'
                      }`}
                    >
                      {isCorrect ? 'Correct!' : 'Incorrect.'}
                    </p>
                    <p className="text-sm text-gray-700 mt-1">
                      {q.explanation}
                    </p>
                    <p className="text-sm text-gray-700 mt-1">
                      {q.difficulty}
                    </p>
                  </div>
                );
              })()}
            </li>
          ))}
        </ul>
      </div>

      {/* --- Final Results Section --- */}
      {isQuizComplete && (
        <>
          {/* Case 1: At least one wrong answer */}
          {wrongAnswerCount > 0 && (
            <div className="mt-6 p-4 bg-yellow-50 border border-yellow-300 rounded-lg">
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Quiz Complete</h3>
              <p className="text-gray-700 mb-3">
                You got {totalQuestions - wrongAnswerCount} out of {totalQuestions} correct.
                Based on the questions you missed, here are some related topics to review:
              </p>
              <div className="flex flex-wrap gap-2 mt-1">
                {quizData.suggested_topics.map((topic, index) => (
                  <span
                    key={index}
                    className="bg-gray-200 text-gray-800 px-3 py-1 rounded-full text-sm font-medium"
                  >
                    {topic}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Case 2: All answers correct */}
          {wrongAnswerCount === 0 && (
            <div className="mt-6 p-4 bg-green-100 border border-green-300 rounded-lg">
              <h3 className="text-xl font-semibold text-green-800 mb-2">Quiz Complete!</h3>
              <p className="text-green-700">
                Congratulations, you got {totalQuestions} out of {totalQuestions} correct!
              </p>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default QuizDisplay;