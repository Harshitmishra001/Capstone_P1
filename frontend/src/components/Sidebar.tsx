import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Layers, FileText, ArrowLeft, Search, Activity, ShieldAlert, BookOpen } from 'lucide-react';

export const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const isCase = location.pathname.startsWith('/incidents/');
  
  // Extract id and tab from the URL if we are in a case
  const pathParts = location.pathname.split('/');
  const caseId = isCase && pathParts.length > 2 ? pathParts[2] : '';
  const currentTab = isCase && pathParts.length > 3 ? pathParts[3] : 'overview';

  return (
    <aside className="w-[230px] bg-[var(--bg-surface)] border-r border-[var(--border-hairline)] flex flex-col p-4">
      <div className="font-['Archivo_Black'] text-[15px] px-2 pb-6">
        SW<span className="text-[var(--accent)]">·</span>
      </div>
      
      <div className="flex flex-col gap-1">
        <button 
          onClick={() => navigate('/')} 
          className="flex items-center gap-3 px-2.5 py-2.5 rounded font-body text-[13px] text-[var(--text-muted)] hover:bg-white/5 hover:text-[var(--text-primary)] transition w-full text-left cursor-pointer"
        >
          <ArrowLeft className="w-[14px] h-[14px] opacity-85 shrink-0" />
          Back to site
        </button>
        
        <button 
          onClick={() => navigate('/dashboard')} 
          className={`flex items-center gap-3 px-2.5 py-2.5 rounded font-body text-[13px] transition w-full text-left cursor-pointer ${location.pathname === '/dashboard' ? 'bg-white/5 text-[var(--text-primary)]' : 'text-[var(--text-muted)] hover:bg-white/5 hover:text-[var(--text-primary)]'}`}
        >
          <Layers className="w-[14px] h-[14px] opacity-85 shrink-0" />
          Cases
        </button>
      </div>

      {isCase && (
        <>
          <div className="text-[10px] tracking-[0.6px] text-[var(--text-muted)] uppercase px-2 pt-6 pb-2">{caseId || 'SW-2024-0142'}</div>
          <div className="flex flex-col gap-1">
            <button 
              onClick={() => navigate(`/incidents/${caseId}/overview`)}
              className={`flex items-center gap-3 px-2.5 py-2.5 rounded font-body text-[13px] transition w-full text-left cursor-pointer ${currentTab === 'overview' ? 'text-[var(--text-primary)] bg-white/5' : 'text-[var(--text-muted)] hover:bg-white/5 hover:text-[var(--text-primary)]'}`}
            >
              <Activity className="w-[14px] h-[14px] opacity-85 shrink-0" />
              Overview
            </button>
            <button 
              onClick={() => navigate(`/incidents/${caseId}/ingestion`)}
              className={`flex items-center gap-3 px-2.5 py-2.5 rounded font-body text-[13px] transition w-full text-left cursor-pointer ${currentTab === 'ingestion' ? 'text-[var(--text-primary)] bg-white/5' : 'text-[var(--text-muted)] hover:bg-white/5 hover:text-[var(--text-primary)]'}`}
            >
              <FileText className="w-[14px] h-[14px] opacity-85 shrink-0" />
              Testimony Ingestion
            </button>
            <button 
              onClick={() => navigate(`/incidents/${caseId}/matrix`)}
              className={`flex items-center gap-3 px-2.5 py-2.5 rounded font-body text-[13px] transition w-full text-left cursor-pointer ${currentTab === 'matrix' ? 'text-[var(--text-primary)] bg-white/5' : 'text-[var(--text-muted)] hover:bg-white/5 hover:text-[var(--text-primary)]'}`}
            >
              <Search className="w-[14px] h-[14px] opacity-85 shrink-0" />
              Spatio-Temporal Matrix
            </button>
            <button 
              onClick={() => navigate(`/incidents/${caseId}/discrepancy`)}
              className={`flex items-center gap-3 px-2.5 py-2.5 rounded font-body text-[13px] transition w-full text-left cursor-pointer ${currentTab === 'discrepancy' ? 'text-[var(--text-primary)] bg-white/5' : 'text-[var(--text-muted)] hover:bg-white/5 hover:text-[var(--text-primary)]'}`}
            >
              <ShieldAlert className="w-[14px] h-[14px] opacity-85 shrink-0" />
              Discrepancy Inspector
            </button>
            <button 
              onClick={() => navigate(`/incidents/${caseId}/dossier`)}
              className={`flex items-center gap-3 px-2.5 py-2.5 rounded font-body text-[13px] transition w-full text-left cursor-pointer ${currentTab === 'dossier' ? 'text-[var(--text-primary)] bg-white/5' : 'text-[var(--text-muted)] hover:bg-white/5 hover:text-[var(--text-primary)]'}`}
            >
              <BookOpen className="w-[14px] h-[14px] opacity-85 shrink-0" />
              Evidentiary Dossier
            </button>
          </div>
        </>
      )}
      
      <div className="mt-auto pt-4 px-2 border-t border-[var(--border-hairline)]">
        <div className="text-[12px] text-[var(--text-muted)]">Signed in as</div>
        <div className="font-['Mrs_Saint_Delafield'] text-[22px] leading-none text-[var(--text-secondary)] mt-1">M. Alvarez</div>
      </div>
    </aside>
  );
};
