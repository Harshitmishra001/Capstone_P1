import React, { useState } from 'react';
import { Upload, Tags, Clock, FileText, User, CheckCircle } from 'lucide-react';
import type { Statement } from '../types';

export const IngestionPanel: React.FC<{ statements: Statement[] }> = ({ statements }) => {
  const [activeTab, setActiveTab] = useState<'text' | 'upload'>('text');

  return (
    <div className="w-[30%] min-w-[320px] max-w-[450px] bg-white border-r border-gray-200 flex flex-col z-10 shadow-[4px_0_10px_rgba(0,0,0,0.03)] shrink-0">
      <div className="p-5 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
        <h2 className="font-bold text-gray-900 text-lg">Testimony Sources</h2>
        <span className="bg-blue-100 text-blue-700 text-xs font-bold px-2 py-1 rounded-full">{statements.length} Processed</span>
      </div>
      
      <div className="p-4 border-b border-gray-200 bg-white">
        <div className="flex rounded-lg border border-gray-200 p-1 bg-gray-50 mb-3">
          <button 
            onClick={() => setActiveTab('text')}
            className={`flex-1 text-sm font-medium py-1.5 rounded-md transition ${activeTab === 'text' ? 'bg-white shadow-sm text-gray-900 border border-gray-200' : 'text-gray-500 hover:text-gray-700'}`}
          >
            Raw Text
          </button>
          <button 
            onClick={() => setActiveTab('upload')}
            className={`flex-1 text-sm font-medium py-1.5 rounded-md transition ${activeTab === 'upload' ? 'bg-white shadow-sm text-gray-900 border border-gray-200' : 'text-gray-500 hover:text-gray-700'}`}
          >
            File Upload
          </button>
        </div>

        {activeTab === 'text' ? (
          <div>
            <textarea className="w-full border border-gray-300 rounded-lg p-3 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 h-32 resize-none placeholder-gray-400" placeholder="Paste witness testimony here..."></textarea>
            <button className="w-full mt-3 bg-gray-900 text-white py-2 rounded-lg text-sm hover:bg-gray-800 shadow-sm transition font-semibold">Extract & Align</button>
          </div>
        ) : (
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 flex flex-col items-center justify-center text-center hover:bg-blue-50 hover:border-blue-300 transition cursor-pointer">
            <Upload className="w-8 h-8 text-blue-500 mb-3" />
            <p className="text-sm font-semibold text-gray-700">Click to upload files</p>
            <p className="text-xs text-gray-500 mt-1">PDF, DOCX, or TXT (max 10MB)</p>
          </div>
        )}
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
        <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3 px-1">Extracted Statements</h3>
        <div className="space-y-3">
          {statements.map(s => (
            <div key={s.id} className="bg-white border border-gray-200 rounded-xl p-4 cursor-pointer hover:border-blue-400 hover:shadow-md transition group">
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-bold text-sm text-gray-900 flex items-center group-hover:text-blue-700 transition">
                  <User className="w-4 h-4 mr-1.5 text-gray-400" />
                  {s.witness}
                </h4>
                <span className="text-[10px] uppercase tracking-wider font-bold text-green-700 bg-green-100 px-2 py-0.5 rounded-full flex items-center">
                  <CheckCircle className="w-3 h-3 mr-1" />
                  {s.status}
                </span>
              </div>
              <div className="text-xs text-gray-600 bg-gray-50 p-2 rounded border border-gray-100 line-clamp-2 italic">
                "{s.text}"
              </div>
              <div className="mt-3 text-[11px] font-medium text-gray-500 flex gap-3">
                <span className="flex items-center bg-gray-100 px-1.5 py-0.5 rounded"><Tags className="mr-1 h-3 w-3 text-blue-500" /> Claims</span>
                <span className="flex items-center bg-gray-100 px-1.5 py-0.5 rounded"><Clock className="mr-1 h-3 w-3 text-purple-500" /> Timeline</span>
                <span className="flex items-center bg-gray-100 px-1.5 py-0.5 rounded"><MapPin className="mr-1 h-3 w-3 text-red-500" /> Map</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
