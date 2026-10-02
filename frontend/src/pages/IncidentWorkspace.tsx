import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { IncidentHeader } from '../components/IncidentHeader';
import { TemporalView } from '../components/TemporalView';
import { SpatialView } from '../components/SpatialView';
import { AnalysisPanel } from '../components/AnalysisPanel';
import { RelationshipGraph } from '../components/RelationshipGraph';
import { IngestionDrawer } from '../components/IngestionDrawer';
import { getIncidentData } from '../api/client';
import { Loader2 } from 'lucide-react';

export const IncidentWorkspace: React.FC = () => {
  const { id, tab = 'overview' } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  
  const [ingestionDrawerOpen, setIngestionDrawerOpen] = useState(false);
  const [focusedEntityId, setFocusedEntityId] = useState<string | undefined>();
  
  // Use route param for active tab
  const activeTab = tab;

  useEffect(() => {
    if (id) {
      setIsLoading(true);
      getIncidentData(id)
        .then(res => {
          setData(res as any);
          setIsLoading(false);
        })
        .catch(() => setIsLoading(false));
    }
  }, [id]);

  const handleExtract = (meta: any, text: string) => {
    console.log("Extracted:", meta, text);
    setIngestionDrawerOpen(false);
  };

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center bg-[var(--bg-base)]">
        <Loader2 className="w-8 h-8 text-[var(--accent)] animate-spin" />
      </div>
    );
  }

  if (!data) {
    return <div className="p-8 text-[var(--text-muted)] font-ui">Incident not found</div>;
  }

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'ingestion', label: 'Testimony Ingestion' },
    { id: 'matrix', label: 'Spatio-Temporal Matrix' },
    { id: 'discrepancy', label: 'Discrepancy Inceptor' },
    { id: 'dossier', label: 'Evidentiary Dossier' }
  ];

  return (
    <div className="h-full flex flex-col bg-[var(--bg-base)] overflow-hidden relative">
      <IncidentHeader id={id || ''} onIngestClick={() => {
        navigate(`/incidents/${id}/ingestion`);
        setIngestionDrawerOpen(true);
      }} />
      
      {/* Tabs Navigation */}
      <div className="flex border-b border-[var(--border-hairline)] bg-[var(--bg-surface)] px-4 shrink-0 overflow-x-auto">
        {tabs.map(t => (
          <button
            key={t.id}
            onClick={() => navigate(`/incidents/${id}/${t.id}`)}
            className={`px-4 py-3 font-ui text-[13px] font-semibold border-b-2 transition-colors whitespace-nowrap cursor-pointer ${activeTab === t.id ? 'border-[var(--accent)] text-[var(--text-primary)]' : 'border-transparent text-[var(--text-muted)] hover:text-[var(--text-secondary)] hover:border-[var(--border-hairline)]'}`}
          >
            {t.label}
          </button>
        ))}
      </div>
      
      {/* Tab Content */}
      <div className="flex-1 overflow-y-auto relative font-body text-[var(--text-primary)]">
        {activeTab === 'overview' && (
          <div className="flex-1 flex flex-col h-full overflow-hidden">
            <TemporalView items={data.timeline} setFocusedEntityId={setFocusedEntityId} />
            <div className="flex-1 flex overflow-hidden">
              <RelationshipGraph />
              <div className="flex-1 flex overflow-hidden">
                <div className="w-[35%] border-r border-[var(--border-hairline)] shrink-0">
                  <SpatialView markers={data.markers} pulsedMarkerId={focusedEntityId} />
                </div>
                <div className="w-[65%] shrink-0">
                  <AnalysisPanel contradictions={data.contradictions} />
                </div>
              </div>
            </div>
          </div>
        )}
        
        {activeTab === 'ingestion' && (
          <div className="max-w-7xl mx-auto p-8">
            <div className="mb-8">
              <h1 className="font-['Hanken_Grotesk'] font-bold text-[26px]">Testimony Ingestion & Claims Extraction</h1>
              <p className="text-[13px] text-[var(--text-muted)] mt-2">Parse depositions, cross-corroborate eyewitness claims, and derive temporal/spatial anchors for review.</p>
            </div>
            
            <div className="grid md:grid-cols-[1.3fr_1fr] gap-8">
              <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6">
                <h2 className="text-[13px] text-[var(--text-muted)] font-semibold mb-4 uppercase tracking-[0.3px]">Source testimony</h2>
                
                <div className="flex gap-2 mb-6">
                  <button className="px-4 py-2 rounded text-[13px] font-semibold bg-[var(--accent)] text-[var(--on-accent)] border border-[var(--accent)]">Paste testimony</button>
                  <button className="px-4 py-2 rounded text-[13px] font-semibold text-[var(--text-muted)] border border-[var(--border-hairline)]">Bulk upload (CSV/JSON)</button>
                  <button className="px-4 py-2 rounded text-[13px] font-semibold text-[var(--text-muted)] border border-[var(--border-hairline)] opacity-40 cursor-not-allowed">Voice dictation</button>
                </div>
                
                <textarea 
                  className="w-full min-h-[120px] bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded p-4 text-[15px] leading-[1.6] resize-y outline-none mb-2 text-[var(--text-primary)]"
                  defaultValue="I was driving north on Main St. when the red sedan ran the red light and clipped the curb near the crosswalk."
                />
                
                <div className="flex justify-between text-[12px] text-[var(--text-muted)] font-mono mb-6">
                  <span>TOKEN COUNT: 34</span>
                  <span>EST. CLAIMS: 4</span>
                </div>
                
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div>
                    <label className="block text-[12px] text-[var(--text-muted)] uppercase tracking-wide mb-2">Witness pseudonym</label>
                    <input type="text" defaultValue="Witness E (Cyclist)" className="w-full bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded px-3 py-2 text-[15px] outline-none text-[var(--text-primary)]" />
                  </div>
                  <div>
                    <label className="block text-[12px] text-[var(--text-muted)] uppercase tracking-wide mb-2">Incident category</label>
                    <input type="text" defaultValue="Road accident" className="w-full bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded px-3 py-2 text-[15px] outline-none text-[var(--text-primary)]" />
                  </div>
                </div>
                
                <button className="w-full py-3 bg-[var(--accent)] text-[var(--on-accent)] font-semibold text-[13px] rounded hover:opacity-90 transition mb-6">
                  Extract & align claims
                </button>
                
                <div className="flex items-center gap-3 p-4 bg-[var(--bg-surface-2)] border border-[var(--border-hairline)] rounded text-[13px] text-[var(--text-secondary)]">
                  <span className="w-1.5 h-1.5 rounded-full bg-[var(--status-corroborate)]"></span>
                  spaCy NER + fastcoref + LLM event-tuple extraction active — 0 synthetic hallucinations flagged
                </div>
              </div>
              
              <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6">
                <h2 className="text-[13px] text-[var(--text-muted)] font-semibold mb-4 uppercase tracking-[0.3px]">Processed statements registry</h2>
                
                <div className="py-4 border-b border-[var(--border-hairline)]">
                  <div className="font-semibold flex justify-between items-center text-[15px]">
                    Witness A (Driver)
                    <span className="text-[12px] px-2 py-0.5 bg-[var(--status-corroborate)]/20 text-[var(--status-corroborate)] rounded-full">processed</span>
                  </div>
                  <div className="text-[13px] text-[var(--text-muted)] mt-1 italic">"...when the <b className="text-[var(--text-primary)]">red sedan</b> ran the red light, right at 14:14..."</div>
                  <div className="flex flex-wrap gap-2 mt-3">
                    <span className="text-[11px] px-2 py-1 border border-[var(--border-hairline)] rounded-sm font-mono text-[var(--text-secondary)]">VEHICLE: RED SEDAN</span>
                    <span className="text-[11px] px-2 py-1 border border-[var(--border-hairline)] rounded-sm font-mono text-[var(--text-secondary)]">ACTION: RAN RED LIGHT</span>
                    <span className="text-[11px] px-2 py-1 border border-[var(--border-hairline)] rounded-sm font-mono text-[var(--text-secondary)]">TIME: 14:14</span>
                  </div>
                </div>
                
                <div className="py-4">
                  <div className="font-semibold flex justify-between items-center text-[15px]">
                    Witness B (Pedestrian)
                    <span className="text-[12px] px-2 py-0.5 bg-[var(--status-corroborate)]/20 text-[var(--status-corroborate)] rounded-full">processed</span>
                  </div>
                  <div className="text-[13px] text-[var(--text-muted)] mt-1 italic">"...the car looked dark, maybe grey, went straight through..."</div>
                  <div className="flex flex-wrap gap-2 mt-3">
                    <span className="text-[11px] px-2 py-1 border border-[var(--border-hairline)] rounded-sm font-mono text-[var(--text-secondary)]">VEHICLE: DARK/GREY</span>
                    <span className="text-[11px] px-2 py-1 border border-[var(--border-hairline)] rounded-sm font-mono text-[var(--text-secondary)]">ACTION: WENT STRAIGHT</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'matrix' && (
          <div className="h-full flex flex-col">
            <TemporalView items={data.timeline} setFocusedEntityId={setFocusedEntityId} />
            <div className="flex-1 border-t border-[var(--border-hairline)] relative">
               <SpatialView markers={data.markers} pulsedMarkerId={focusedEntityId} />
            </div>
          </div>
        )}

        {activeTab === 'discrepancy' && (
          <div className="max-w-7xl mx-auto p-8">
            <div className="flex justify-between items-start mb-8">
              <div>
                <h1 className="font-['Hanken_Grotesk'] font-bold text-[26px]">Discrepancy Inspector</h1>
                <p className="text-[15px] mt-2">Target variable: <b className="text-[var(--text-primary)]">Direction of travel</b></p>
              </div>
              <span className="text-[11px] px-3 py-1 border border-[var(--accent)] text-[var(--accent)] rounded-full font-bold">FR11 · Full traceability</span>
            </div>
            
            <div className="grid md:grid-cols-[1.3fr_1fr] gap-8">
              <div>
                <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6 mb-4">
                  <div className="flex justify-between text-[12px] text-[var(--text-muted)] mb-4 font-semibold tracking-wide">
                    <span>WITNESS A (DRIVER) · DEPO #1</span>
                    <span>PARA 1, LINE 2</span>
                  </div>
                  <blockquote className="text-[17px] leading-[1.6] italic">
                    "...it was <mark className="bg-[var(--status-contradict)]/20 text-[var(--status-contradict)] px-1 rounded">turning left</mark> onto 9th when it clipped..."
                  </blockquote>
                </div>
                
                <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6">
                  <div className="flex justify-between text-[12px] text-[var(--text-muted)] mb-4 font-semibold tracking-wide">
                    <span>WITNESS B (PEDESTRIAN) · DEPO #2</span>
                    <span>PARA 1, LINE 1</span>
                  </div>
                  <blockquote className="text-[17px] leading-[1.6] italic">
                    "...the car <mark className="bg-[var(--status-contradict)]/20 text-[var(--status-contradict)] px-1 rounded">went straight through</mark> the junction."
                  </blockquote>
                </div>
              </div>
              
              <div>
                <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6 mb-6">
                  <h2 className="text-[13px] text-[var(--text-muted)] font-semibold mb-4 uppercase tracking-[0.3px]">Coreference resolution</h2>
                  <p className="text-[13px] text-[var(--text-secondary)]">
                    Merged entity cluster <b className="text-[var(--text-primary)]">#E-12 "vehicle in collision"</b> — 2 references unified across statements.
                  </p>
                </div>
                
                <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6 mb-6">
                  <h2 className="text-[13px] text-[var(--text-muted)] font-semibold mb-4 uppercase tracking-[0.3px]">Contradiction likelihood</h2>
                  <div className="h-1.5 bg-[var(--bg-base)] rounded-full overflow-hidden my-4">
                    <div className="h-full bg-[var(--status-contradict)]" style={{ width: '91%' }}></div>
                  </div>
                  <p className="text-[12px] text-[var(--text-muted)]">
                    p(contradiction) = 0.91 · RoBERTa-large-MNLI + isotonic calibration
                  </p>
                </div>
                
                <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6">
                  <p className="text-[13px] text-[var(--text-muted)] border-l-2 border-[var(--accent)] pl-4 leading-[1.6]">
                    This indicates a factual mismatch between two accounts — not a judgement on which witness is correct.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'dossier' && (
          <div className="max-w-7xl mx-auto p-8">
            <div className="mb-8">
              <h1 className="font-['Hanken_Grotesk'] font-bold text-[26px]">Evidentiary Dossier</h1>
              <p className="text-[13px] text-[var(--text-muted)] mt-2">Export a consolidated, cryptographically chained findings report for this case.</p>
            </div>
            
            <div className="grid grid-cols-3 gap-6 mb-8">
              <button className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6 text-left hover:border-[var(--accent)] transition-colors cursor-pointer group">
                <div className="text-[17px] font-semibold mb-2 group-hover:text-[var(--accent)] transition-colors">Evidentiary Dossier</div>
                <div className="text-[13px] text-[var(--text-muted)]">Full PDF — statements, timeline, flags</div>
              </button>
              <button className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6 text-left hover:border-[var(--accent)] transition-colors cursor-pointer group">
                <div className="text-[17px] font-semibold mb-2 group-hover:text-[var(--accent)] transition-colors">Claim Graph</div>
                <div className="text-[13px] text-[var(--text-muted)]">Neo4j-compatible JSON export</div>
              </button>
              <button className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6 text-left hover:border-[var(--accent)] transition-colors cursor-pointer group">
                <div className="text-[17px] font-semibold mb-2 group-hover:text-[var(--accent)] transition-colors">Summary</div>
                <div className="text-[13px] text-[var(--text-muted)]">CSV of flags & corroborations</div>
              </button>
            </div>
            
            <div className="grid md:grid-cols-[1.3fr_1fr] gap-8">
              <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6">
                <h2 className="text-[13px] text-[var(--text-muted)] font-semibold mb-4 uppercase tracking-[0.3px]">Corroboration matrix</h2>
                
                <div className="py-4 border-b border-[var(--border-hairline)]">
                  <div className="font-semibold flex justify-between items-center text-[15px]">
                    Point of impact agreement
                    <span className="text-[12px] px-2 py-0.5 bg-[var(--status-corroborate)]/20 text-[var(--status-corroborate)] rounded-full">3/3 witnesses</span>
                  </div>
                  <div className="text-[13px] text-[var(--text-muted)] mt-1">All accounts place the collision at the 9th & Laurel intersection. Zero spatial variance.</div>
                </div>
                
                <div className="py-4">
                  <div className="font-semibold flex justify-between items-center text-[15px]">
                    Vehicle colour — red
                    <span className="text-[12px] px-2 py-0.5 bg-[var(--status-corroborate)]/20 text-[var(--status-corroborate)] rounded-full">2/3 witnesses</span>
                  </div>
                  <div className="text-[13px] text-[var(--text-muted)] mt-1">Witnesses A and C independently describe a red vehicle.</div>
                </div>
              </div>
              
              <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6 h-fit">
                <h2 className="text-[13px] text-[var(--text-muted)] font-semibold mb-4 uppercase tracking-[0.3px]">Chain of custody</h2>
                <div className="bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded p-4 font-mono text-[12px] text-[var(--text-secondary)] break-all mb-4">
                  SHA256:7f83b1e7ff9d1c5e3e2b...e692fabc — Immutable ledger v4.8
                </div>
                <p className="text-[13px] text-[var(--text-muted)]">
                  Every export is hash-chained to the source statements it was derived from, for defensible audit review.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      <IngestionDrawer 
        isOpen={ingestionDrawerOpen} 
        onClose={() => setIngestionDrawerOpen(false)} 
        onExtract={handleExtract}
      />
    </div>
  );
};
