import React from 'react';
import { Download, Share2, Upload } from 'lucide-react';

export const IncidentHeader: React.FC<{ id: string, onIngestClick: () => void }> = ({ id, onIngestClick }) => {
  return (
    <div className="h-16 border-b border-[var(--border-hairline)] bg-[var(--bg-surface)] flex items-center justify-between px-6 shrink-0">
      <div className="flex items-center">
        <h2 className="text-lg font-ui font-semibold text-[var(--text-primary)]">Main St Collision</h2>
        <span className="ml-3 px-2 py-0.5 bg-[var(--bg-surface-2)] border border-[var(--border-hairline)] text-[var(--text-muted)] text-xs font-mono rounded">
          ID: {id}
        </span>
        <span className="ml-3 px-2 py-0.5 text-[var(--status-partial)] border border-[var(--status-partial)] bg-[var(--status-partial)]/10 text-xs font-mono font-medium rounded uppercase tracking-wider">
          Reviewing
        </span>
      </div>
      <div className="flex space-x-3">
        <button 
          onClick={onIngestClick}
          className="border border-[var(--border-hairline)] bg-[var(--bg-surface)] hover:bg-[var(--bg-surface-2)] text-[var(--text-primary)] px-3 py-1.5 rounded text-sm font-ui flex items-center transition-colors focus-bracket cursor-pointer"
        >
          <Upload className="w-4 h-4 mr-2" /> Ingest Data
        </button>
        <button className="border border-[var(--border-hairline)] bg-[var(--bg-surface)] hover:bg-[var(--bg-surface-2)] text-[var(--text-secondary)] px-3 py-1.5 rounded text-sm font-ui flex items-center transition-colors focus-bracket cursor-pointer">
          <Share2 className="w-4 h-4 mr-2" /> Share
        </button>
        <button className="border border-[var(--border-hairline)] bg-[var(--bg-surface)] hover:bg-[var(--bg-surface-2)] text-[var(--text-secondary)] px-3 py-1.5 rounded text-sm font-ui flex items-center transition-colors focus-bracket cursor-pointer">
          <Download className="w-4 h-4 mr-2" /> Export
        </button>
      </div>
    </div>
  );
};
