import React, { useState } from 'react';
import { Maximize2, Search, X, CheckCircle } from 'lucide-react';
import type { Contradiction } from '../types';

const TraceSidePanel: React.FC<{ trace: any, onClose: () => void }> = ({ trace, onClose }) => {
  if (!trace) return null;
  return (
    <div className="absolute top-0 right-0 bottom-0 w-[400px] bg-[var(--bg-surface-2)] border-l border-[var(--border-hairline)] flex flex-col z-20 shadow-2xl transition-transform">
      <div className="h-10 border-b border-[var(--border-hairline)] px-3 flex items-center justify-between shrink-0">
        <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase tracking-wider flex items-center">
          <Search className="w-3.5 h-3.5 mr-2" />
          Source Trace
        </span>
        <button onClick={onClose} className="text-[var(--text-muted)] hover:text-[var(--text-primary)] transition p-1 hover:bg-[var(--bg-surface)] rounded cursor-pointer focus-bracket">
          <X className="w-4 h-4" />
        </button>
      </div>
      <div className="p-4 flex-1 overflow-y-auto">
        <div className="mb-4">
          <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase tracking-wider block mb-1">Witness</span>
          <span className="font-ui font-semibold text-[var(--text-primary)] text-sm px-2 py-0.5 bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded">{trace.witness}</span>
        </div>
        <div className="bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded p-4 font-body text-[var(--text-secondary)] text-[13px] leading-relaxed">
          {trace.fullText.substring(0, trace.span[0])}
          <span className="bg-[var(--accent)]/20 text-[var(--accent)] font-semibold px-1 rounded-sm border border-[var(--accent)]/50 mx-0.5">
            {trace.fullText.substring(trace.span[0], trace.span[1])}
          </span>
          {trace.fullText.substring(trace.span[1])}
        </div>
      </div>
    </div>
  );
};

const ContradictionCard: React.FC<{ c: Contradiction, onTraceClick: (claim: any) => void }> = ({ c, onTraceClick }) => {
  const [expanded, setExpanded] = useState(false);
  const colorVar = c.type === 'Unverified' ? 'var(--status-unverified)' : 'var(--status-contradict)';

  return (
    <div className="border border-[var(--border-hairline)] bg-[var(--bg-surface)] rounded flex flex-col relative focus-within:border-[var(--accent)] transition-colors">
      <div className="absolute left-0 top-0 bottom-0 w-1 rounded-l" style={{ backgroundColor: colorVar }} />
      <div 
        className="px-4 py-3 cursor-pointer select-none flex items-center justify-between pl-5 hover:bg-[var(--bg-surface-2)] transition-colors focus-bracket"
        onClick={() => setExpanded(!expanded)}
        tabIndex={0}
        onKeyDown={(e) => { if (e.key === 'Enter') setExpanded(!expanded); }}
      >
        <div>
          <h4 className="font-ui font-semibold text-[var(--text-primary)] text-sm">{c.title}</h4>
          <p className="font-ui text-xs text-[var(--text-secondary)] mt-0.5 line-clamp-1">{c.rationale}</p>
        </div>
        <span className="text-[10px] font-mono font-bold uppercase tracking-wider border px-2 py-0.5 rounded ml-4 shrink-0" style={{ color: colorVar, borderColor: colorVar, backgroundColor: `color-mix(in srgb, ${colorVar} 10%, transparent)` }}>
          {c.type}
        </span>
      </div>
      {expanded && (
        <div className="px-5 pb-4 pt-1 border-t border-[var(--border-hairline)] bg-[var(--bg-base)]">
          <div className="mt-3 grid grid-cols-1 gap-3">
            {c.claims.map((claim, idx) => (
              <div key={idx} className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded p-3 flex flex-col items-start relative group">
                <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase tracking-wider mb-2">{claim.witness}</span>
                <p className="font-body text-xs text-[var(--text-primary)] italic">"{claim.snippet}"</p>
                <button 
                  onClick={(e) => { e.stopPropagation(); onTraceClick(claim); }}
                  className="absolute top-2 right-2 text-[var(--text-muted)] hover:text-[var(--accent)] p-1 rounded hover:bg-[var(--bg-surface-2)] transition-colors opacity-0 group-hover:opacity-100 cursor-pointer focus-bracket"
                  title="View full trace"
                >
                  <Search className="w-3.5 h-3.5" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export const AnalysisPanel: React.FC<{ contradictions: Contradiction[] }> = ({ contradictions }) => {
  const [activeTrace, setActiveTrace] = useState<any>(null);

  return (
    <div className="h-full w-full relative flex flex-col bg-[var(--bg-base)] overflow-hidden">
      <div className="h-10 border-b border-[var(--border-hairline)] bg-[var(--bg-surface-2)] px-3 flex items-center justify-between z-10 shrink-0">
        <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase tracking-wider">Analysis Payoff</span>
        <div className="flex space-x-1">
          <button className="text-[var(--text-muted)] hover:text-[var(--text-primary)] transition p-1 hover:bg-[var(--bg-surface)] rounded cursor-pointer focus-bracket"><Maximize2 className="w-3.5 h-3.5" /></button>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
        <div className="space-y-3">
          {contradictions.map(c => (
            <ContradictionCard key={c.id} c={c} onTraceClick={setActiveTrace} />
          ))}
          {contradictions.length === 0 && (
            <div className="text-center py-10">
              <CheckCircle className="w-8 h-8 text-[var(--status-corroborate)] mx-auto mb-2 opacity-80" />
              <p className="font-ui text-sm text-[var(--text-secondary)]">No conflicts detected.</p>
            </div>
          )}
        </div>
      </div>

      <TraceSidePanel trace={activeTrace} onClose={() => setActiveTrace(null)} />
    </div>
  );
};
