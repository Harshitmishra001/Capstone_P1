import React, { useState, useEffect } from 'react';
import { X, CheckCircle2, Loader2, ArrowRight } from 'lucide-react';

export const IngestionDrawer: React.FC<{ 
  isOpen: boolean, 
  onClose: () => void, 
  onExtract: (meta: any, text: string) => void 
}> = ({ isOpen, onClose, onExtract }) => {
  const [witnessName, setWitnessName] = useState('');
  const [date, setDate] = useState('');
  const [location, setLocation] = useState('');
  const [rawText, setRawText] = useState('');
  
  const [isProcessing, setIsProcessing] = useState(false);
  const [stepIndex, setStepIndex] = useState(0);
  const steps = [
    "Parsing entities...",
    "Aligning timeline...",
    "Cross-referencing...",
    "Detecting contradictions..."
  ];

  useEffect(() => {
    let timer: any;
    if (isProcessing && stepIndex < steps.length) {
      timer = setTimeout(() => {
        setStepIndex(stepIndex + 1);
      }, 1000); // fake progression for UX
    } else if (isProcessing && stepIndex === steps.length) {
      onExtract({ witnessName, date, location }, rawText);
      setIsProcessing(false);
      setStepIndex(0);
      onClose();
    }
    return () => clearTimeout(timer);
  }, [isProcessing, stepIndex]);

  const handleSubmit = () => {
    if (!rawText.trim() || !witnessName.trim()) return;
    setIsProcessing(true);
    setStepIndex(0);
  };

  const wordCount = rawText.trim().split(/\s+/).filter(w => w.length > 0).length;
  let parseability = "";
  if (wordCount === 0) parseability = "";
  else if (wordCount < 20) parseability = "Very short — extraction may be limited";
  else if (wordCount > 200) parseability = "Looks like a clear narrative";
  else parseability = "Sufficient for extraction";

  return (
    <div className={`fixed inset-y-0 right-0 w-[500px] bg-[var(--bg-surface-2)] border-l border-[var(--border-hairline)] shadow-2xl z-40 transform transition-transform duration-200 ${isOpen ? 'translate-x-0' : 'translate-x-full'} flex flex-col`}>
      <div className="h-16 border-b border-[var(--border-hairline)] px-6 flex items-center justify-between shrink-0 bg-[var(--bg-surface)]">
        <h2 className="text-lg font-ui font-semibold text-[var(--text-primary)]">Ingest Testimony</h2>
        <button onClick={onClose} className="text-[var(--text-muted)] hover:text-[var(--text-primary)] transition p-1 hover:bg-[var(--bg-surface-2)] rounded cursor-pointer focus-bracket">
          <X className="w-5 h-5" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-5">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-[10px] font-mono text-[var(--text-secondary)] mb-1.5 uppercase tracking-wider">Witness Name / ID</label>
            <input type="text" value={witnessName} onChange={e => setWitnessName(e.target.value)} disabled={isProcessing} className="w-full bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded px-3 py-2 text-sm font-ui text-[var(--text-primary)] focus:border-[var(--accent)] outline-none" />
          </div>
          <div>
            <label className="block text-[10px] font-mono text-[var(--text-secondary)] mb-1.5 uppercase tracking-wider">Date of Statement</label>
            <input type="date" value={date} onChange={e => setDate(e.target.value)} disabled={isProcessing} className="w-full bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded px-3 py-2 text-sm font-mono text-[var(--text-primary)] focus:border-[var(--accent)] outline-none [color-scheme:dark]" />
          </div>
          <div className="col-span-2">
            <label className="block text-[10px] font-mono text-[var(--text-secondary)] mb-1.5 uppercase tracking-wider">Location</label>
            <input type="text" value={location} onChange={e => setLocation(e.target.value)} disabled={isProcessing} className="w-full bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded px-3 py-2 text-sm font-ui text-[var(--text-primary)] focus:border-[var(--accent)] outline-none" />
          </div>
        </div>

        <div>
          <div className="flex justify-between items-end mb-1.5">
            <label className="block text-[10px] font-mono text-[var(--text-secondary)] uppercase tracking-wider">Statement Transcript</label>
            {wordCount > 0 && (
              <span className="text-[10px] font-mono text-[var(--text-muted)]">{wordCount} words &bull; <span className={wordCount < 20 ? 'text-[var(--status-partial)]' : 'text-[var(--status-corroborate)]'}>{parseability}</span></span>
            )}
          </div>
          <textarea 
            className="w-full h-64 bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded p-3 text-sm font-body text-[var(--text-primary)] focus:border-[var(--accent)] outline-none resize-none custom-scrollbar" 
            placeholder="Paste raw transcript or statement here..."
            value={rawText}
            onChange={e => setRawText(e.target.value)}
            disabled={isProcessing}
          />
        </div>
      </div>

      <div className="p-6 border-t border-[var(--border-hairline)] bg-[var(--bg-surface)] shrink-0">
        {isProcessing ? (
          <div className="space-y-3">
            <h4 className="text-xs font-mono text-[var(--text-primary)] uppercase tracking-wider mb-2">Processing Pipeline</h4>
            {steps.map((step, idx) => (
              <div key={idx} className={`flex items-center text-sm font-ui ${idx < stepIndex ? 'text-[var(--status-corroborate)]' : idx === stepIndex ? 'text-[var(--accent)]' : 'text-[var(--text-muted)]'}`}>
                {idx < stepIndex ? <CheckCircle2 className="w-4 h-4 mr-2" /> : idx === stepIndex ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <div className="w-4 h-4 mr-2 border border-[var(--border-hairline)] rounded-full" />}
                {step}
              </div>
            ))}
          </div>
        ) : (
          <button 
            onClick={handleSubmit}
            disabled={!rawText.trim() || !witnessName.trim()}
            className="w-full bg-[var(--text-primary)] text-[var(--bg-base)] font-ui font-semibold text-sm py-2.5 rounded hover:bg-[var(--text-primary)]/90 transition-colors cursor-pointer focus-bracket disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            Run Extraction <ArrowRight className="w-4 h-4 ml-2" />
          </button>
        )}
      </div>
    </div>
  );
};
