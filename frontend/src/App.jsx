import React, { useState } from 'react';
import GenerateQuizTab from './tabs/GenerateQuizTab';
import HistoryTab from './tabs/HistoryTab';

function App() {
  const [activeTab, setActiveTab] = useState('generate');

  const TabButton = ({ tabId, children }) => (
    <button
      className={`py-2 px-6 rounded-t-lg text-lg font-medium transition-colors ${
        activeTab === tabId
          ? 'bg-blue-600 text-white'
          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
      }`}
      onClick={() => setActiveTab(tabId)}
    >
      {children}
    </button>
  );

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-gray-800 mb-8">
          AI Quiz Generator
        </h1>
        
        {/* Tab Navigation */}
        <nav className="flex justify-center">
          <TabButton tabId="generate">Generate New Quiz</TabButton>
          <TabButton tabId="history">History</TabButton>
        </nav>

        {/* Tab Content */}
        <main className="bg-white p-6 shadow-xl rounded-b-lg rounded-tr-lg">
          {activeTab === 'generate' && <GenerateQuizTab />}
          {activeTab === 'history' && <HistoryTab />}
        </main>
      </div>
    </div>
  );
}

export default App;
