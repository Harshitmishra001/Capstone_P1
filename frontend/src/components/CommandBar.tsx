import React, { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const CommandBar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
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

  if (!isOpen) return null;

  const mockResults = [
    { type: 'Witness', name: 'Witness A (Driver)', id: 'wit_0' },
    { type: 'Entity', name: 'Red Sedan', id: 'ent_1' },
    { type: 'Case', name: 'Main St Collision', id: 'inc-101' },
  ].filter(r => r.name.toLowerCase().includes(query.toLowerCase()));

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-start justify-center pt-[15vh]">
      <div className="w-full max-w-2xl bg-[var(--bg-surface-2)] border border-[var(--border-hairline)] rounded shadow-2xl overflow-hidden flex flex-col">
        <div className="flex items-center px-4 border-b border-[var(--border-hairline)]">
          <Search className="w-5 h-5 text-[var(--text-muted)] mr-3" />
          <input 
            autoFocus
            type="text" 
            className="flex-1 bg-transparent text-[var(--text-primary)] font-mono text-sm py-4 outline-none placeholder:text-[var(--text-muted)]"
            placeholder="Search witnesses, entities, case IDs... (Esc to close)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
        {query && (
          <div className="max-h-64 overflow-y-auto py-2">
            {mockResults.map((res, i) => (
              <button 
                key={i}
                className="w-full text-left px-4 py-3 flex items-center hover:bg-[var(--bg-surface)] focus:bg-[var(--bg-surface)] outline-none focus-bracket cursor-pointer"
                onClick={() => {
                  setIsOpen(false);
                  if (res.type === 'Case') navigate(`/incidents/${res.id}`);
                }}
              >
                <span className="text-xs font-mono text-[var(--accent)] w-20 uppercase">{res.type}</span>
                <span className="font-ui text-sm text-[var(--text-primary)] ml-2">{res.name}</span>
                <span className="ml-auto text-xs font-mono text-[var(--text-muted)]">{res.id}</span>
              </button>
            ))}
            {mockResults.length === 0 && (
              <div className="px-4 py-8 text-center text-[var(--text-muted)] font-ui text-sm">
                No results found.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
