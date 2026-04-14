import React, { useState, useEffect } from 'react';
import axios from 'axios';
import BugForm from '../components/BugForm';
import BugList from '../components/BugList';

const API_BASE = 'http://localhost:5000/api';

export default function Dashboard() {
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
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-6 py-4">
        <h1 className="text-xl font-bold text-blue-600">BugFlow</h1>
      </nav>
      <main className="max-w-7xl mx-auto py-6 px-4 space-y-8">
        <BugForm onCreated={handleBugCreated} />
        <BugList bugs={bugs} onUpdated={handleBugUpdated} />
      </main>
    </div>
  );
}
