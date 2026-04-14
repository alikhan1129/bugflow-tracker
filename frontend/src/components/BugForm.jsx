import React, { useState } from 'react';
import axios from 'axios';

const API_BASE = '/api';

const BugForm = ({ onCreated }) => {
  const [formData, setFormData] = useState({ title: '', description: '', useAi: true });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/bugs`, { 
        title: formData.title, 
        description: formData.description, 
        use_ai_triage: formData.useAi 
      });
      onCreated(res.data);
      setFormData({ title: '', description: '', useAi: true });
    } catch (err) { 
      alert(err.response?.data?.error || 'Error'); 
    } finally { 
      setLoading(false); 
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
          <input 
            required 
            value={formData.title} 
            onChange={e => setFormData({...formData, title: e.target.value})} 
            className="w-full px-4 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all placeholder:text-gray-400 shadow-sm" 
            placeholder="Issue title" 
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea 
            required 
            rows={3} 
            value={formData.description} 
            onChange={e => setFormData({...formData, description: e.target.value})} 
            className="w-full px-4 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all placeholder:text-gray-400 resize-none shadow-sm" 
            placeholder="Describe the problem..." 
          />
        </div>
        <div className="flex items-center gap-2">
          <input 
            id="ai-triage"
            type="checkbox" 
            checked={formData.useAi} 
            onChange={e => setFormData({...formData, useAi: e.target.checked})} 
            className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 cursor-pointer" 
          />
          <label htmlFor="ai-triage" className="text-sm font-medium text-gray-600 cursor-pointer">
            Enable AI Triage
          </label>
        </div>
      </div>
      <button 
        disabled={loading} 
        className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:opacity-90 text-white font-medium py-2.5 px-4 rounded-lg transition-all shadow-md active:scale-[0.99] disabled:opacity-70"
      >
        {loading ? 'Processing...' : 'Report Bug'}
      </button>
    </form>
  );
};

export default BugForm;
