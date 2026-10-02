import React, { useEffect, useState } from 'react';
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
    <div className="p-8 pb-12 font-body text-[var(--text-primary)]">
      <div className="flex items-start justify-between mb-8 flex-wrap gap-4">
        <div>
          <h1 className="font-['Hanken_Grotesk'] font-bold text-[26px]">Cases</h1>
          <p className="text-[13px] text-[var(--text-muted)] mt-2">5 incidents · 2 awaiting review</p>
        </div>
        <button className="px-[18px] py-[10px] bg-[var(--accent)] text-[var(--bg-base)] font-semibold text-[13px] rounded flex items-center">
          New incident
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6">
          <div className="font-['Archivo_Black'] text-[34px] leading-none">5</div>
          <div className="text-[12px] text-[var(--text-muted)] mt-2 uppercase tracking-wide">Active cases</div>
        </div>
        <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6">
          <div className="font-['Archivo_Black'] text-[34px] leading-none">21</div>
          <div className="text-[12px] text-[var(--text-muted)] mt-2 uppercase tracking-wide">Claims extracted</div>
        </div>
        <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6">
          <div className="font-['Archivo_Black'] text-[34px] leading-none">7</div>
          <div className="text-[12px] text-[var(--text-muted)] mt-2 uppercase tracking-wide">Flags raised</div>
        </div>
        <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6">
          <div className="font-['Archivo_Black'] text-[34px] leading-none">100%</div>
          <div className="text-[12px] text-[var(--text-muted)] mt-2 uppercase tracking-wide">Source traceable</div>
        </div>
      </div>

      <div className="border-t border-[var(--border-hairline)]">
        {incidents.map((incident, idx) => (
          <button 
            key={incident.id} 
            onClick={() => navigate(`/incidents/${incident.id}`)}
            className="w-full grid grid-cols-[120px_1fr_130px_150px_150px_110px] items-center gap-4 px-2 py-4 border-b border-[var(--border-hairline)] text-[15px] text-left hover:bg-white/5 transition-colors cursor-pointer"
          >
            <span className="font-mono text-[12px] text-[var(--text-muted)]">{incident.id}</span>
            <span className="font-semibold">{incident.title}<small className="block font-normal text-[var(--text-muted)] text-[13px] mt-0.5">{incident.witnessCount} witness statements</small></span>
            <span className="inline-block text-[12px] px-2.5 py-1 rounded-full border border-[var(--border-hairline)] text-[var(--text-muted)] w-max">{incident.type}</span>
            <span className="text-[13px] flex items-center gap-2 text-[var(--text-secondary)]">
              {incident.contradictionCount > 0 ? (
                <><span className="w-1.5 h-1.5 rounded-full bg-[var(--status-contradict)]"></span>{incident.contradictionCount} contradictions</>
              ) : (
                <><span className="w-1.5 h-1.5 rounded-full bg-[var(--text-muted)]"></span>Processing</>
              )}
            </span>
            <span className="text-[13px] flex items-center gap-2 text-[var(--text-secondary)]">
              <span className="w-1.5 h-1.5 rounded-full bg-[var(--status-corroborate)]"></span>
              {idx === 0 ? '3 corroborated' : idx === 2 ? '5 corroborated' : 'Reviewed'}
            </span>
            <span className="text-[12px] text-[var(--text-muted)] font-mono">{incident.date}</span>
          </button>
        ))}
      </div>
    </div>
  );
};
