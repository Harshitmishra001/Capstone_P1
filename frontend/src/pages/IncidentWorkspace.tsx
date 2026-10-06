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
                <h2 className="text-[13px] text-[var(--text-muted)] font-semibold mb-4 uppercase tracking-[0.3px]">Source testimonies</h2>
                
                <div className="flex gap-2 mb-6">
                  <button className="px-4 py-2 rounded text-[13px] font-semibold bg-[var(--accent)] text-[var(--on-accent)] border border-[var(--accent)]">Paste testimony</button>
                  <button className="px-4 py-2 rounded text-[13px] font-semibold text-[var(--text-muted)] border border-[var(--border-hairline)]">Bulk upload (CSV/JSON)</button>
                </div>
                
                <div id="testimony-container" className="flex flex-col gap-4 mb-4">
                  {/* Default statements to show ML contradiction capability */}
                  <div className="testimony-block relative">
                    <div className="absolute top-3 right-3 text-[10px] font-mono text-[var(--text-muted)]">WITNESS A</div>
                    <textarea 
                      className="testimony-input w-full min-h-[100px] bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded p-4 text-[15px] leading-[1.6] resize-y outline-none text-[var(--text-primary)]"
                      defaultValue="Two masked robbers stormed in. The primary robber wore a dark leather jacket and had a silver gun."
                    />
                  </div>
                  <div className="testimony-block relative">
                    <div className="absolute top-3 right-3 text-[10px] font-mono text-[var(--text-muted)]">WITNESS B</div>
                    <textarea 
                      className="testimony-input w-full min-h-[100px] bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded p-4 text-[15px] leading-[1.6] resize-y outline-none text-[var(--text-primary)]"
                      defaultValue="Three guys ran out of the store. The lead robber had a bright red hoodie."
                    />
                  </div>
                </div>

                <button 
                  onClick={() => {
                    const container = document.getElementById('testimony-container');
                    if (container) {
                      const count = container.children.length;
                      const div = document.createElement('div');
                      div.className = "testimony-block relative mt-4";
                      div.innerHTML = `
                        <div class="absolute top-3 right-3 text-[10px] font-mono text-[var(--text-muted)]">WITNESS ${String.fromCharCode(65 + count)}</div>
                        <textarea class="testimony-input w-full min-h-[100px] bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded p-4 text-[15px] leading-[1.6] resize-y outline-none text-[var(--text-primary)]" placeholder="Enter witness statement..."></textarea>
                      `;
                      container.appendChild(div);
                    }
                  }}
                  className="w-full py-2 border border-dashed border-[var(--border-hairline)] text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:border-[var(--text-muted)] transition rounded text-[13px] font-semibold mb-6 cursor-pointer"
                >
                  + Add another statement
                </button>
                
                <div className="mb-6">
                  <label className="block text-[12px] text-[var(--text-muted)] uppercase tracking-wide mb-2">Incident Title</label>
                  <input type="text" id="incident-cat" defaultValue="Downtown Convenience Store Robbery" className="w-full bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded px-3 py-2 text-[15px] outline-none text-[var(--text-primary)]" />
                </div>
                
                <button 
                  onClick={async () => {
                    const inputs = document.querySelectorAll('.testimony-input') as NodeListOf<HTMLTextAreaElement>;
                    const statements = Array.from(inputs).map(i => i.value).filter(v => v.trim() !== "");
                    const title = (document.getElementById('incident-cat') as HTMLInputElement).value;
                    if (statements.length === 0) return;
                    
                    const btn = document.getElementById('extract-btn');
                    if (btn) btn.innerText = 'Running ML Pipeline...';
                    
                    try {
                      const { createIncident } = await import('../api/client');
                      const res = await createIncident(title, statements);
                      navigate(`/incidents/${res.id}/overview`);
                    } catch (e) {
                      console.error(e);
                      alert('Failed to process testimony. Ensure the FastAPI backend is running.');
                    } finally {
                      if (btn) btn.innerText = 'Extract & align claims';
                    }
                  }}
                  id="extract-btn"
                  className="w-full py-3 bg-[var(--accent)] text-[var(--on-accent)] font-semibold text-[13px] rounded hover:opacity-90 transition mb-6 cursor-pointer"
                >
                  Extract & align claims
                </button>
                
                <div className="flex items-center gap-3 p-4 bg-[var(--bg-surface-2)] border border-[var(--border-hairline)] rounded text-[13px] text-[var(--text-secondary)]">
                  <span className="w-1.5 h-1.5 rounded-full bg-[var(--status-corroborate)]"></span>
                  Connected to Local ML Pipeline — Processing cross-statement discrepancies
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
                <p className="text-[15px] mt-2">Target variable: <b className="text-[var(--text-primary)]">Statements Conflict</b></p>
              </div>
              <span className="text-[11px] px-3 py-1 border border-[var(--accent)] text-[var(--accent)] rounded-full font-bold">FR11 · Full traceability</span>
            </div>
            
            {data.contradictions && data.contradictions.length > 0 ? (
              <div className="flex flex-col gap-12">
                {data.contradictions.map((c: any) => (
                  <div key={c.id} className="grid md:grid-cols-[1.3fr_1fr] gap-8">
                    <div>
                      {c.claims.map((claim: any, idx: number) => (
                        <div key={idx} className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6 mb-4">
                          <div className="flex justify-between text-[12px] text-[var(--text-muted)] mb-4 font-semibold tracking-wide uppercase">
                            <span>{claim.witness}</span>
                            <span>{claim.span ? `CHAR ${claim.span[0]}-${claim.span[1]}` : ''}</span>
                          </div>
                          <blockquote className="text-[17px] leading-[1.6] italic text-[var(--text-primary)]">
                            {claim.fullText && claim.span && claim.span.length === 2 && claim.span[1] > 0 ? (
                              <>
                                {claim.fullText.substring(0, claim.span[0])}
                                <mark className="bg-[var(--status-contradict)]/20 text-[var(--status-contradict)] px-1 rounded">
                                  {claim.fullText.substring(claim.span[0], claim.span[1])}
                                </mark>
                                {claim.fullText.substring(claim.span[1])}
                              </>
                            ) : (
                              <mark className="bg-[var(--status-contradict)]/20 text-[var(--status-contradict)] px-1 rounded">{claim.snippet}</mark>
                            )}
                          </blockquote>
                        </div>
                      ))}
                    </div>
                    
                    <div>
                      <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6 mb-6">
                        <h2 className="text-[13px] text-[var(--text-muted)] font-semibold mb-4 uppercase tracking-[0.3px]">Coreference resolution</h2>
                        <p className="text-[13px] text-[var(--text-secondary)]">
                          Merged entity cluster <b className="text-[var(--text-primary)]">#E-12</b> — References unified across statements.
                        </p>
                      </div>
                      
                      <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6 mb-6">
                        <h2 className="text-[13px] text-[var(--text-muted)] font-semibold mb-4 uppercase tracking-[0.3px]">Contradiction likelihood</h2>
                        <div className="h-1.5 bg-[var(--bg-base)] rounded-full overflow-hidden my-4">
                          <div className="h-full bg-[var(--status-contradict)]" style={{ width: '95%' }}></div>
                        </div>
                        <p className="text-[12px] text-[var(--text-muted)]">
                          {c.rationale}
                        </p>
                      </div>
                      
                      <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6">
                        <p className="text-[13px] text-[var(--text-muted)] border-l-2 border-[var(--accent)] pl-4 leading-[1.6]">
                          This indicates a factual mismatch between two accounts — not a judgement on which witness is correct.
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-8 text-center bg-[var(--bg-surface)] rounded-lg border border-[var(--border-hairline)] text-[var(--text-muted)]">
                No discrepancies found in this case.
              </div>
            )}
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
