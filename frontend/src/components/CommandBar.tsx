import React, { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { getIncidents } from '../api/client';
import type { IncidentSummary } from '../types';

export const CommandBar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [incidents, setIncidents] = useState<IncidentSummary[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen(true);
      }
      if (e.key === 'Escape') {
        setIsOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  useEffect(() => {
    if (isOpen) {
      getIncidents().then(data => setIncidents(data)).catch(() => {});
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const q = query.trim().toLowerCase();
  const searchResults = incidents
    .filter(inc => 
      !q || 
      inc.title.toLowerCase().includes(q) || 
      inc.id.toLowerCase().includes(q) || 
      inc.type.toLowerCase().includes(q)
    )
    .map(inc => ({
      type: 'Case',
      name: inc.title,
      id: inc.id,
      subtitle: `${inc.type} • ${inc.witnessCount} witnesses • ${inc.status}`
    }));

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-start justify-center pt-[15vh]">
      <div className="w-full max-w-2xl bg-[var(--bg-surface-2)] border border-[var(--border-hairline)] rounded shadow-2xl overflow-hidden flex flex-col">
        <div className="flex items-center px-4 border-b border-[var(--border-hairline)]">
          <Search className="w-5 h-5 text-[var(--text-muted)] mr-3" />
          <input 
            autoFocus
            type="text" 
            className="flex-1 bg-transparent text-[var(--text-primary)] font-mono text-sm py-4 outline-none placeholder:text-[var(--text-muted)]"
            placeholder="Search cases by title, ID, or crime type... (Esc to close)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
        {query && (
          <div className="max-h-64 overflow-y-auto py-2">
            {searchResults.map((res, i) => (
              <button 
                key={i}
                className="w-full text-left px-4 py-3 flex items-center hover:bg-[var(--bg-surface)] focus:bg-[var(--bg-surface)] outline-none focus-bracket cursor-pointer"
                onClick={() => {
                  setIsOpen(false);
                  navigate(`/incidents/${res.id}/overview`);
                }}
              >
                <span className="text-xs font-mono text-[var(--accent)] w-16 uppercase shrink-0">{res.type}</span>
                <div className="ml-2 flex-1 min-w-0">
                  <div className="font-ui text-sm text-[var(--text-primary)] truncate">{res.name}</div>
                  <div className="text-xs text-[var(--text-muted)]">{res.subtitle}</div>
                </div>
                <span className="ml-3 text-xs font-mono text-[var(--text-muted)] shrink-0">{res.id}</span>
              </button>
            ))}
            {searchResults.length === 0 && (
              <div className="px-4 py-8 text-center text-[var(--text-muted)] font-ui text-sm">
                No cases found matching "{query}".
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
