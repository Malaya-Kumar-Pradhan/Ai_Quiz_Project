import React from 'react';
import { X } from 'lucide-react';

function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 backdrop-filter backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-white w-full max-w-2xl max-h-[80vh] p-6 rounded-lg shadow-xl relative overflow-y-auto" 
        onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside
      >
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-500 hover:text-gray-800 transition-colors"
        >
          <X size={20} />
        </button>
        <div className="mt-8">
          {children}
        </div>
      </div>
    </div>
  );
}

export default Modal;