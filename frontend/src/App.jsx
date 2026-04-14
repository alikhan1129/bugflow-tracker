import React, { useState, useEffect } from 'react';
import axios from 'axios';
import BugForm from './components/BugForm';
import BugList from './components/BugList';

const API_BASE = '/api';

export default function App() {
  const [bugs, setBugs] = useState([]);

  const fetchBugs = async () => {
    try {
      const res = await axios.get(`${API_BASE}/bugs`);
      setBugs(res.data);
    } catch (err) {
      console.error('Error fetching bugs:', err);
    }
  };

  useEffect(() => { 
    fetchBugs(); 
  }, []);

  const handleBugCreated = (newBug) => {
    setBugs(prevBugs => [newBug, ...prevBugs]);
  };

  const handleBugUpdated = (updatedBug) => {
    setBugs(prevBugs => prevBugs.map(b => b.id === updatedBug.id ? updatedBug : b));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-gray-200 py-12 px-4">
      <div className="max-w-4xl mx-auto bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-6 space-y-6">
        <header className="space-y-1">
          <h1 className="text-3xl font-bold text-gray-900">BugFlow</h1>
          <p className="text-gray-500 text-sm">AI-powered bug tracking system</p>
        </header>

        <main className="space-y-6">
          <BugForm onCreated={handleBugCreated} />
          <BugList bugs={bugs} onUpdated={handleBugUpdated} />
        </main>
      </div>
    </div>
  );
}
