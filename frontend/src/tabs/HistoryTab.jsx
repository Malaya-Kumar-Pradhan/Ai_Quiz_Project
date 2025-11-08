import React, { useState, useEffect } from 'react';
import { Loader2 } from 'lucide-react';
import * as api from '../services/api.js';

// The component subfolder paths
import Modal from "../components/Modal/Modal.jsx";
import QuizDetailView from '../components/QuizCard/QuizDetailView.jsx';
import HistoryTable from "../components/HistoryTable.jsx";

function HistoryTab() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedQuizId, setSelectedQuizId] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await api.getHistory();

        // We will sort the array by ID in ascending order (1, 2, 3...)
        // We use [...data] to create a copy before sorting
        const sortedData = [...data].sort((a, b) => a.id - b.id);

        setHistory(sortedData); // Set the newly sorted array

      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []); // This still only runs once, which is correct

  const handleDetailsClick = (id) => {
    setSelectedQuizId(id);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedQuizId(null);
  };

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

  return (
    <>
      <HistoryTable 
        history={history} 
        onDetailsClick={handleDetailsClick} 
      />

      <Modal isOpen={isModalOpen} onClose={handleCloseModal}>
        {selectedQuizId && <QuizDetailView quizId={selectedQuizId} />}
      </Modal>
    </>
  );
}

export default HistoryTab;