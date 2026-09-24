import React, { useState } from 'react';
import { AlertCircle, CheckCircle, Search, X, MapPin, Clock, Tag } from 'lucide-react';
import type { Contradiction } from '../types';

export const AnalysisPanel: React.FC<{ contradictions: Contradiction[] }> = ({ contradictions }) => {
  const [activeTab, setActiveTab] = useState<'contradictions' | 'corroborations'>('contradictions');
  const [activeTrace, setActiveTrace] = useState<any>(null);
  
  return (
    <div className="flex-1 bg-white flex flex-col min-h-0 relative">
      <div className="flex border-b border-gray-200 bg-gray-50 px-2 pt-2 shrink-0">
        <button 
          onClick={() => setActiveTab('contradictions')}
          className={`px-4 py-2 text-sm font-semibold rounded-t-lg transition ${activeTab === 'contradictions' ? 'bg-white text-red-600 border-t border-l border-r border-gray-200 shadow-[0_-2px_0_0_#ef4444]' : 'text-gray-500 hover:bg-gray-100'}`}
        >
          <div className="flex items-center"><AlertCircle className="w-4 h-4 mr-2" /> Contradictions ({contradictions.length})</div>
        </button>
        <button 
          onClick={() => setActiveTab('corroborations')}
          className={`px-4 py-2 text-sm font-semibold rounded-t-lg transition ${activeTab === 'corroborations' ? 'bg-white text-green-600 border-t border-l border-r border-gray-200 shadow-[0_-2px_0_0_#22c55e]' : 'text-gray-500 hover:bg-gray-100'}`}
        >
          <div className="flex items-center"><CheckCircle className="w-4 h-4 mr-2" /> Corroborations (5)</div>
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto p-6 bg-gray-50/50">
        {activeTab === 'contradictions' && (
          <div className="space-y-6 max-w-5xl mx-auto">
            {contradictions.map(c => (
              <div key={c.id} className="border border-red-200 rounded-xl overflow-hidden shadow-sm bg-white transition hover:shadow-md">
                <div className="bg-red-50/80 px-5 py-3 border-b border-red-100 flex justify-between items-center">
                  <div className="flex items-center">
                    <AlertCircle className="text-red-500 w-5 h-5 mr-3" />
                    <h4 className="font-semibold text-red-900 text-lg">{c.title}</h4>
                    <span className="ml-4 text-xs bg-red-100 text-red-700 px-2.5 py-1 rounded-full font-bold uppercase tracking-wider flex items-center">
                      {c.type === 'Temporal' && <Clock className="w-3 h-3 mr-1" />}
                      {c.type === 'Attribute' && <Tag className="w-3 h-3 mr-1" />}
                      {c.type} Mismatch
                    </span>
                  </div>
                  <div className="space-x-2">
                    <button className="text-sm font-medium text-gray-600 hover:bg-white hover:text-gray-900 border border-gray-300 px-3 py-1.5 rounded-lg transition">Acknowledge</button>
                    <button className="text-sm font-medium text-white bg-red-600 hover:bg-red-700 px-3 py-1.5 rounded-lg transition shadow-sm">Flag for Review</button>
                  </div>
                </div>
                <div className="p-5">
                  <p className="text-sm text-gray-700 mb-5 font-medium border-l-4 border-gray-200 pl-3 py-1">{c.rationale}</p>
                  <div className="grid grid-cols-2 gap-6">
                    {c.claims.map((claim, idx) => {
                      const prefix = claim.fullText.substring(0, claim.span[0]);
                      const match = claim.fullText.substring(claim.span[0], claim.span[1]);
                      const suffix = claim.fullText.substring(claim.span[1]);
                      
                      return (
                        <div key={idx} className="bg-gray-50 p-4 rounded-lg border border-gray-200 relative group hover:border-blue-300 transition cursor-pointer" onClick={() => setActiveTrace(claim)}>
                          <h5 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">{claim.witness}</h5>
                          <p className="text-sm text-gray-800 leading-relaxed italic line-clamp-3">
                            "{prefix}<span className="bg-yellow-200 font-semibold px-1 rounded mx-0.5 shadow-sm text-black">{match}</span>{suffix}"
                          </p>
                          <div className="absolute top-3 right-3 text-blue-500 opacity-0 group-hover:opacity-100 transition bg-blue-50 p-1.5 rounded-md border border-blue-200">
                            <Search className="w-4 h-4" />
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Traceability Modal */}
      {activeTrace && (
        <div className="absolute inset-0 bg-gray-900/40 backdrop-blur-sm z-50 flex items-center justify-center">
          <div className="bg-white rounded-xl shadow-2xl w-[600px] max-w-full overflow-hidden transform transition-all">
            <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
              <h3 className="font-bold text-gray-900 flex items-center">
                <Search className="w-5 h-5 mr-2 text-blue-500" />
                Source Traceability
              </h3>
              <button onClick={() => setActiveTrace(null)} className="text-gray-400 hover:text-gray-700 p-1 rounded-lg hover:bg-gray-200 transition">
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="p-6">
              <div className="mb-4">
                <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Source Document</span>
                <p className="font-semibold text-gray-900">{activeTrace.witness}</p>
              </div>
              <div className="bg-blue-50/50 border border-blue-100 p-5 rounded-lg text-gray-800 leading-loose text-[15px]">
                {activeTrace.fullText.substring(0, activeTrace.span[0])}
                <span className="bg-yellow-300 font-bold px-1.5 py-0.5 rounded shadow-sm text-black mx-0.5">
                  {activeTrace.fullText.substring(activeTrace.span[0], activeTrace.span[1])}
                </span>
                {activeTrace.fullText.substring(activeTrace.span[1])}
              </div>
              <div className="mt-6 flex justify-end">
                <button onClick={() => setActiveTrace(null)} className="bg-gray-900 text-white px-5 py-2 rounded-lg text-sm font-medium hover:bg-gray-800 transition">Close Trace</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
