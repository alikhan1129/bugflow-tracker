import React, { useState } from 'react';
import axios from 'axios';

const API_BASE = '/api';

const BugList = ({ bugs, onUpdated }) => {
  const [notes, setNotes] = useState({ id: null, text: '' });

  const updateStatus = async (bug, next) => {
    if (next === 'CLOSED' && !notes.text && !bug.resolution_notes) return setNotes({ id: bug.id, text: '' });
    try {
      const res = await axios.patch(`${API_BASE}/bugs/${bug.id}`, { 
        status: next, 
        resolution_notes: notes.text || bug.resolution_notes 
      });
      onUpdated(res.data);
      setNotes({ id: null, text: '' });
    } catch (err) { 
      alert(err.response?.data?.error || 'Error'); 
    }
  };

  const getSeverityStyles = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-700';
      case 'medium': return 'bg-yellow-100 text-yellow-700';
      case 'low': return 'bg-green-100 text-green-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  if (bugs.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 space-y-2">
        <p className="text-gray-400 text-lg font-medium">No bugs reported yet 🚀</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {bugs.map(bug => (
        <div key={bug.id} className="bg-white p-4 rounded-xl border border-gray-100 shadow-md hover:shadow-lg hover:scale-[1.01] transition-all group">
          <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
            <div className="flex-1 space-y-3">
              <div className="space-y-1">
                <h4 className="text-lg font-bold text-gray-900 group-hover:text-blue-600 transition-colors">{bug.title}</h4>
                <p className="text-gray-500 text-sm leading-relaxed">{bug.description}</p>
              </div>
              
              <div className="flex flex-wrap items-center gap-2">
                <span className="px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-600">
                  {bug.status.replace('_', ' ')}
                </span>
                {bug.severity && (
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getSeverityStyles(bug.severity)}`}>
                    {bug.severity}
                  </span>
                )}
                {bug.category && (
                  <span className="px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-700">
                    {bug.category}
                  </span>
                )}
              </div>

              {bug.resolution_notes && (
                <div className="p-3 bg-gray-50 rounded-lg border border-gray-100 text-sm text-gray-600 italic">
                  <span className="font-semibold text-gray-900 not-italic mr-2">Fixed:</span> {bug.resolution_notes}
                </div>
              )}
            </div>

            <div className="flex-shrink-0">
              {notes.id === bug.id ? (
                <div className="w-full md:w-64 space-y-2">
                  <textarea 
                    className="w-full p-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all shadow-sm" 
                    placeholder="Enter fix details..." 
                    value={notes.text} 
                    onChange={e => setNotes({...notes, text: e.target.value})} 
                  />
                  <div className="flex gap-2">
                    <button onClick={() => setNotes({id: null, text: ''})} className="px-3 py-1 text-xs font-medium text-gray-500 hover:text-gray-700">Cancel</button>
                    <button 
                      onClick={() => updateStatus(bug, 'CLOSED')} 
                      className="flex-1 bg-gray-900 hover:bg-black text-white px-3 py-1.5 rounded-lg text-xs font-bold transition-all shadow-sm"
                    >
                      Confirm Close
                    </button>
                  </div>
                </div>
              ) : (
                ['OPEN', 'IN_PROGRESS', 'RESOLVED'].includes(bug.status) && (
                  <button 
                    onClick={() => updateStatus(bug, { OPEN: 'IN_PROGRESS', IN_PROGRESS: 'RESOLVED', RESOLVED: 'CLOSED' }[bug.status])} 
                    className="w-full md:w-auto px-4 py-2 bg-white border border-gray-300 hover:border-blue-600 hover:text-blue-600 text-gray-700 rounded-lg text-sm font-semibold transition-all shadow-sm active:scale-[0.98]"
                  >
                    Move to { { OPEN: 'In Progress', IN_PROGRESS: 'Resolved', RESOLVED: 'Closed' }[bug.status] }
                  </button>
                )
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default BugList;
