import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ChevronLeft } from 'lucide-react';
import { IngestionPanel } from '../components/IngestionPanel';
import { SpatialView } from '../components/SpatialView';
import { TemporalView } from '../components/TemporalView';
import { AnalysisPanel } from '../components/AnalysisPanel';
import { getIncidentData } from '../api/client';
import type { Statement, MapMarker, TimelineItem, Contradiction } from '../types';

export const IncidentWorkspace: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<{
    statements: Statement[];
    markers: MapMarker[];
    timeline: TimelineItem[];
    contradictions: Contradiction[];
  } | null>(null);

  useEffect(() => {
    if (id) {
      getIncidentData(id).then(setData);
    }
  }, [id]);

  if (!data) return <div className="flex items-center justify-center h-full text-slate-500 font-semibold">Loading workspace...</div>;

  return (
    <div className="flex-1 flex flex-col md:flex-row overflow-hidden">
      <IngestionPanel statements={data.statements} />
      
      {/* Main visualization area */}
      <div className="flex-1 flex flex-col min-w-0 bg-gray-100">
        
        {/* Workspace Toolbar */}
        <div className="bg-white border-b border-gray-200 px-4 py-2 flex items-center shadow-sm z-10 shrink-0">
          <Link to="/" className="text-gray-500 hover:text-blue-600 mr-4 flex items-center text-sm font-medium transition">
            <ChevronLeft className="w-4 h-4 mr-1" /> Back
          </Link>
          <div className="h-4 w-px bg-gray-300 mr-4"></div>
          <span className="font-semibold text-gray-800 text-sm">Incident Workspace: <span className="text-blue-600 font-mono">{id}</span></span>
        </div>

        {/* Top half: Map and Timeline side-by-side */}
        <div className="flex h-[45%] min-h-[300px]">
          <div className="w-[40%] border-r border-gray-200 shadow-sm z-10 relative">
            <SpatialView markers={data.markers} />
          </div>
          <div className="w-[60%] relative bg-white border-b border-gray-200">
            <TemporalView items={data.timeline} />
          </div>
        </div>
        
        {/* Bottom half: Analysis Panel */}
        <AnalysisPanel contradictions={data.contradictions} />
        
      </div>
    </div>
  );
};
