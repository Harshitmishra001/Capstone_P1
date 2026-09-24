import React, { useEffect, useState } from 'react';
import { Plus, Search, Filter } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { getIncidents } from '../api/client';
import type { IncidentSummary } from '../types';

export const Dashboard: React.FC = () => {
  const [incidents, setIncidents] = useState<IncidentSummary[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    getIncidents().then(setIncidents);
  }, []);

  return (
    <div className="p-8 h-full overflow-y-auto bg-gray-50">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Incidents Dashboard</h1>
          <p className="text-gray-500 text-sm mt-1">Manage and analyze eyewitness testimony alignments.</p>
        </div>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium flex items-center transition shadow-sm">
          <Plus className="w-5 h-5 mr-2" />
          New Incident
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50/50">
          <div className="relative w-64">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input 
              type="text" 
              placeholder="Search incidents..." 
              className="w-full pl-9 pr-4 py-2 rounded-lg border border-gray-300 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
            />
          </div>
          <button className="text-gray-600 hover:text-gray-900 flex items-center text-sm font-medium border border-gray-300 rounded-lg px-3 py-2 bg-white hover:bg-gray-50 transition">
            <Filter className="w-4 h-4 mr-2" /> Filter
          </button>
        </div>
        
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider border-b border-gray-200">
              <th className="px-6 py-4 font-semibold">Incident Title</th>
              <th className="px-6 py-4 font-semibold">Type</th>
              <th className="px-6 py-4 font-semibold">Date</th>
              <th className="px-6 py-4 font-semibold">Status</th>
              <th className="px-6 py-4 font-semibold text-center">Witnesses</th>
              <th className="px-6 py-4 font-semibold text-center">Contradictions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {incidents.map(inc => (
              <tr 
                key={inc.id} 
                onClick={() => navigate(`/incidents/${inc.id}`)}
                className="hover:bg-blue-50/50 cursor-pointer transition group"
              >
                <td className="px-6 py-4">
                  <div className="font-semibold text-gray-900 group-hover:text-blue-700 transition">{inc.title}</div>
                  <div className="text-xs text-gray-500 mt-1 font-mono">{inc.id}</div>
                </td>
                <td className="px-6 py-4 text-sm text-gray-600">{inc.type}</td>
                <td className="px-6 py-4 text-sm text-gray-600">{inc.date}</td>
                <td className="px-6 py-4">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                    inc.status === 'Active' ? 'bg-green-100 text-green-700' : 
                    inc.status === 'Reviewing' ? 'bg-yellow-100 text-yellow-700' : 
                    'bg-gray-100 text-gray-600'
                  }`}>
                    {inc.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-center font-medium text-gray-700">{inc.witnessCount}</td>
                <td className="px-6 py-4 text-sm text-center">
                  {inc.contradictionCount > 0 ? (
                    <span className="bg-red-100 text-red-700 px-2 py-1 rounded text-xs font-bold shadow-sm">{inc.contradictionCount} Flags</span>
                  ) : (
                    <span className="text-gray-400 font-medium text-xs">Clean</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
