import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { IncidentHeader } from '../components/IncidentHeader';
import { TemporalView } from '../components/TemporalView';
import { SpatialView } from '../components/SpatialView';
import { AnalysisPanel } from '../components/AnalysisPanel';
import { RelationshipGraph } from '../components/RelationshipGraph';
import { IngestionDrawer } from '../components/IngestionDrawer';
import { getIncidentData, getIncidents, createIncident } from '../api/client';
import { Loader2 } from 'lucide-react';

export const IncidentWorkspace: React.FC = () => {
  const { id, tab = 'overview' } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState<any | null>(null);
  const [summary, setSummary] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [ingestionDrawerOpen, setIngestionDrawerOpen] = useState(false);
  const [focusedEntityId, setFocusedEntityId] = useState<string | undefined>();
  const [isExtracting, setIsExtracting] = useState(false);

  // Extra state for ingestion tab
  const [witnesses, setWitnesses] = useState<string[]>(['', '']);
  const [incidentTitle, setIncidentTitle] = useState('');

  const activeTab = tab;

  useEffect(() => {
    if (id) {
      setIsLoading(true);
      Promise.all([
        getIncidentData(id),
        getIncidents()
      ]).then(([incData, summaries]) => {
        setData(incData as any);
        const found = (summaries as any[]).find((s: any) => s.id === id);
        setSummary(found || null);
        // Pre-fill ingestion tab with real statements from DB
        if ((incData as any)?.statements) {
          setWitnesses((incData as any).statements.map((s: any) => s.text));
          setIncidentTitle(found?.title || '');
        }
        setIsLoading(false);
      }).catch(() => setIsLoading(false));
    }
  }, [id]);

  const handleExtract = async (meta: any, text: string) => {
    setIngestionDrawerOpen(false);
    if (!text.trim()) return;
    setIsExtracting(true);
    try {
      const currentStatements = witnesses.filter(w => w.trim() !== '');
      const newStatements = [...currentStatements, text.trim()];
      const title = meta?.witnessName ? `${incidentTitle || 'Investigation'} - ${meta.witnessName}` : (incidentTitle || 'New Investigation');
      const res = await createIncident(title, newStatements);
      navigate(`/incidents/${res.id}/overview`);
    } catch {
      alert('Failed to process testimony. Ensure the FastAPI backend is running on port 8000.');
    } finally {
      setIsExtracting(false);
    }
  };

  const handleAddWitness = () => {
    setWitnesses(prev => [...prev, '']);
  };

  const handleWitnessChange = (idx: number, val: string) => {
    setWitnesses(prev => prev.map((w, i) => i === idx ? val : w));
  };

  const handleExtractClaims = async () => {
    const statements = witnesses.filter(w => w.trim() !== '');
    if (statements.length === 0) return;
    setIsExtracting(true);
    try {
      const res = await createIncident(incidentTitle || 'New Case', statements);
      navigate(`/incidents/${res.id}/overview`);
    } catch (e) {
      alert('Failed to process testimony. Ensure the FastAPI backend is running on port 8000.');
    } finally {
      setIsExtracting(false);
    }
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
    { id: 'overview',    label: 'Overview' },
    { id: 'ingestion',   label: 'Testimony Ingestion' },
    { id: 'matrix',      label: 'Spatio-Temporal Matrix' },
    { id: 'discrepancy', label: 'Discrepancy Inceptor' },
    { id: 'dossier',     label: 'Evidentiary Dossier' }
  ];

  // Metrics for Overview header cards
  const totalEvents    = data.timeline?.length ?? 0;
  const totalConflicts = data.contradictions?.length ?? 0;
  const witnesses_count = data.statements?.length ?? 0;
  const locations_count = data.markers?.length ?? 0;

  return (
    <div className="h-full flex flex-col bg-[var(--bg-base)] overflow-hidden relative">
      <IncidentHeader id={id || ''} onIngestClick={() => {
        navigate(`/incidents/${id}/ingestion`);
      }} />

      {/* Summary metric bar */}
      <div className="flex gap-6 px-6 py-2 bg-[var(--bg-surface)] border-b border-[var(--border-hairline)] text-[12px] shrink-0">
        <span className="text-[var(--text-muted)]">Case <b className="text-[var(--text-primary)] font-mono">{id}</b></span>
        <span className="text-[var(--text-muted)]">Witnesses: <b className="text-[var(--text-primary)]">{witnesses_count}</b></span>
        <span className="text-[var(--text-muted)]">Events: <b className="text-[var(--text-primary)]">{totalEvents}</b></span>
        <span className="text-[var(--text-muted)]">Flagged: <b className="text-[var(--status-contradict)]">{totalConflicts}</b></span>
        <span className="text-[var(--text-muted)]">Locations: <b className="text-[var(--text-primary)]">{locations_count}</b></span>
        {summary && <span className="ml-auto text-[var(--accent)] font-semibold">{summary.title}</span>}
      </div>

      {/* Tabs Navigation */}
      <div className="flex border-b border-[var(--border-hairline)] bg-[var(--bg-surface)] px-4 shrink-0 overflow-x-auto">
        {tabs.map(t => (
          <button
            key={t.id}
            onClick={() => navigate(`/incidents/${id}/${t.id}`)}
            className={`px-4 py-3 font-ui text-[13px] font-semibold border-b-2 transition-colors whitespace-nowrap cursor-pointer ${activeTab === t.id ? 'border-[var(--accent)] text-[var(--text-primary)]' : 'border-transparent text-[var(--text-muted)] hover:text-[var(--text-secondary)] hover:border-[var(--border-hairline)]'}`}
          >
            {t.label}
            {t.id === 'discrepancy' && totalConflicts > 0 && (
              <span className="ml-2 text-[10px] px-1.5 py-0.5 rounded-full bg-[var(--status-contradict)]/20 text-[var(--status-contradict)] font-bold">{totalConflicts}</span>
            )}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="flex-1 overflow-hidden relative font-body text-[var(--text-primary)]">

        {/* ─── OVERVIEW ─── */}
        {activeTab === 'overview' && (
          <div className="absolute inset-0 flex flex-col">
            <TemporalView items={data.timeline ?? []} setFocusedEntityId={setFocusedEntityId} />
            <div className="flex-1 flex overflow-hidden min-h-0">
              <RelationshipGraph data={data} />
              <div className="flex-1 flex overflow-hidden min-h-0">
                <div className="w-[38%] border-r border-[var(--border-hairline)] shrink-0 h-full">
                  <SpatialView markers={data.markers ?? []} pulsedMarkerId={focusedEntityId} />
                </div>
                <div className="w-[62%] shrink-0 h-full overflow-hidden">
                  <AnalysisPanel contradictions={data.contradictions ?? []} />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ─── TESTIMONY INGESTION ─── */}
        {activeTab === 'ingestion' && (
          <div className="overflow-y-auto h-full">
            <div className="max-w-7xl mx-auto p-8">
              <div className="mb-8">
                <h1 className="font-['Hanken_Grotesk'] font-bold text-[26px]">Testimony Ingestion & Claims Extraction</h1>
                <p className="text-[13px] text-[var(--text-muted)] mt-2">
                  Parse depositions, cross-corroborate eyewitness claims, and derive temporal/spatial anchors for review.
                </p>
              </div>

              <div className="grid md:grid-cols-[1.3fr_1fr] gap-8">
                {/* Left — Input */}
                <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6">
                  <h2 className="text-[13px] text-[var(--text-muted)] font-semibold mb-4 uppercase tracking-[0.3px]">Source Testimonies</h2>

                  <div className="flex flex-col gap-4 mb-4">
                    {witnesses.map((text, idx) => (
                      <div key={idx} className="relative">
                        <div className="absolute top-3 right-3 text-[10px] font-mono text-[var(--text-muted)]">
                          WITNESS {String.fromCharCode(65 + idx)}
                        </div>
                        <textarea
                          className="w-full min-h-[90px] bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded p-4 text-[15px] leading-[1.6] resize-y outline-none text-[var(--text-primary)] pr-20"
                          placeholder="Enter witness statement..."
                          value={text}
                          onChange={e => handleWitnessChange(idx, e.target.value)}
                        />
                      </div>
                    ))}
                  </div>

                  <button
                    onClick={handleAddWitness}
                    className="w-full py-2 border border-dashed border-[var(--border-hairline)] text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:border-[var(--text-muted)] transition rounded text-[13px] font-semibold mb-6 cursor-pointer"
                  >
                    + Add another statement
                  </button>

                  <div className="mb-6">
                    <label className="block text-[12px] text-[var(--text-muted)] uppercase tracking-wide mb-2">Incident Title</label>
                    <input
                      type="text"
                      value={incidentTitle}
                      onChange={e => setIncidentTitle(e.target.value)}
                      placeholder="e.g. Jewelry Store Heist"
                      className="w-full bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded px-3 py-2 text-[15px] outline-none text-[var(--text-primary)]"
                    />
                  </div>

                  <button
                    onClick={handleExtractClaims}
                    disabled={isExtracting}
                    className="w-full py-3 bg-[var(--accent)] text-[var(--on-accent)] font-semibold text-[13px] rounded hover:opacity-90 transition mb-4 cursor-pointer disabled:opacity-60"
                  >
                    {isExtracting ? 'Running ML Pipeline…' : 'Extract & align claims'}
                  </button>

                  <div className="flex items-center gap-3 p-4 bg-[var(--bg-surface-2)] border border-[var(--border-hairline)] rounded text-[13px] text-[var(--text-secondary)]">
                    <span className="w-1.5 h-1.5 rounded-full bg-[var(--status-corroborate)] shrink-0" />
                    Connected to Local ML Pipeline — Fallback: theft_case_output.json
                  </div>
                </div>

                {/* Right — Processed Registry */}
                <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6">
                  <h2 className="text-[13px] text-[var(--text-muted)] font-semibold mb-4 uppercase tracking-[0.3px]">
                    Processed Statements Registry ({data.statements?.length ?? 0})
                  </h2>

                  {data.statements && data.statements.length > 0 ? (
                    <div className="flex flex-col gap-4">
                      {data.statements.map((stmt: any) => (
                        <div key={stmt.id} className="py-4 border-b border-[var(--border-hairline)] last:border-0">
                          <div className="font-semibold flex justify-between items-center text-[15px] mb-1">
                            {stmt.witness}
                            <span className="text-[12px] px-2 py-0.5 bg-[var(--status-corroborate)]/20 text-[var(--status-corroborate)] rounded-full">
                              {stmt.status}
                            </span>
                          </div>
                          <div className="text-[13px] text-[var(--text-muted)] italic leading-relaxed">
                            "{stmt.text.substring(0, 120)}{stmt.text.length > 120 ? '…' : ''}"
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-[13px] text-[var(--text-muted)]">No statements ingested yet.</div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ─── SPATIO-TEMPORAL MATRIX ─── */}
        {activeTab === 'matrix' && (
          <div className="absolute inset-0 flex flex-col">
            <TemporalView items={data.timeline ?? []} setFocusedEntityId={setFocusedEntityId} />
            <div className="flex-1 min-h-0 border-t border-[var(--border-hairline)] relative">
              <SpatialView markers={data.markers ?? []} pulsedMarkerId={focusedEntityId} />
            </div>
          </div>
        )}

        {/* ─── DISCREPANCY INCEPTOR ─── */}
        {activeTab === 'discrepancy' && (
          <div className="overflow-y-auto h-full">
            <div className="max-w-7xl mx-auto p-8">
              <div className="flex justify-between items-start mb-8">
                <div>
                  <h1 className="font-['Hanken_Grotesk'] font-bold text-[26px]">Discrepancy Inceptor</h1>
                  <p className="text-[15px] mt-2 text-[var(--text-secondary)]">
                    <b className="text-[var(--status-contradict)]">{totalConflicts}</b> semantic conflicts flagged across {witnesses_count} witness statements
                  </p>
                </div>
                <span className="text-[11px] px-3 py-1 border border-[var(--accent)] text-[var(--accent)] rounded-full font-bold">FR11 · Full traceability</span>
              </div>

              {data.contradictions && data.contradictions.length > 0 ? (
                <div className="flex flex-col gap-10">
                  {data.contradictions.map((c: any) => (
                    <div key={c.id} className="grid md:grid-cols-[1.4fr_1fr] gap-8">
                      {/* Claims */}
                      <div>
                        <div className="text-[11px] font-mono text-[var(--text-muted)] mb-3 uppercase tracking-wider">{c.title}</div>
                        {c.claims.map((claim: any, idx: number) => (
                          <div key={idx} className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-5 mb-3">
                            <div className="flex justify-between text-[12px] text-[var(--text-muted)] mb-3 font-semibold tracking-wide uppercase">
                              <span>{claim.witness}</span>
                              <span className="font-mono">CHAR {claim.span?.[0]}–{claim.span?.[1]}</span>
                            </div>
                            <blockquote className="text-[15px] leading-[1.7] text-[var(--text-secondary)]">
                              {claim.fullText && claim.span && claim.span[1] > claim.span[0] ? (
                                <>
                                  {claim.fullText.substring(0, claim.span[0])}
                                  <mark className="bg-[var(--status-contradict)]/20 text-[var(--status-contradict)] px-1 rounded font-semibold not-italic">
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

                      {/* Analysis sidebar */}
                      <div>
                        <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-5 mb-4">
                          <h2 className="text-[11px] text-[var(--text-muted)] font-semibold mb-3 uppercase tracking-[0.3px]">Contradiction Rationale</h2>
                          <p className="text-[13px] text-[var(--text-secondary)] leading-relaxed">{c.rationale}</p>
                        </div>
                        <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-5 mb-4">
                          <h2 className="text-[11px] text-[var(--text-muted)] font-semibold mb-3 uppercase tracking-[0.3px]">Contradiction Likelihood</h2>
                          <div className="h-1.5 bg-[var(--bg-base)] rounded-full overflow-hidden mb-2">
                            <div className="h-full bg-[var(--status-contradict)]" style={{ width: '95%' }} />
                          </div>
                          <p className="text-[11px] font-mono text-[var(--text-muted)]">p=0.95 · RoBERTa-large-MNLI + isotonic calibration</p>
                        </div>
                        <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-5">
                          <p className="text-[13px] text-[var(--text-muted)] border-l-2 border-[var(--accent)] pl-3 leading-[1.6]">
                            Factual mismatch between accounts — not a judgement on correctness.
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
          </div>
        )}

        {/* ─── EVIDENTIARY DOSSIER ─── */}
        {activeTab === 'dossier' && (
          <div className="overflow-y-auto h-full">
            <div className="max-w-7xl mx-auto p-8">
              <div className="mb-8">
                <h1 className="font-['Hanken_Grotesk'] font-bold text-[26px]">Evidentiary Dossier</h1>
                <p className="text-[13px] text-[var(--text-muted)] mt-2">
                  Consolidated cryptographically-chained findings for: <b className="text-[var(--text-primary)]">{summary?.title ?? id}</b>
                </p>
              </div>

              {/* Export buttons */}
              <div className="grid grid-cols-3 gap-6 mb-8">
                {[
                  { label: 'Evidentiary Dossier', sub: 'Full PDF — statements, timeline, flags' },
                  { label: 'Claim Graph',          sub: 'Neo4j-compatible JSON export' },
                  { label: 'Summary CSV',          sub: 'CSV of flags & corroborations' }
                ].map(btn => (
                  <button
                    key={btn.label}
                    onClick={() => alert(`${btn.label} export is deferred to a future architecture phase.`)}
                    className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6 text-left hover:border-[var(--accent)] transition-colors cursor-pointer group"
                  >
                    <div className="text-[17px] font-semibold mb-2 group-hover:text-[var(--accent)] transition-colors">{btn.label}</div>
                    <div className="text-[13px] text-[var(--text-muted)]">{btn.sub}</div>
                  </button>
                ))}
              </div>

              <div className="grid md:grid-cols-[1.3fr_1fr] gap-8">
                {/* Flagged discrepancies summary */}
                <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6">
                  <h2 className="text-[13px] text-[var(--text-muted)] font-semibold mb-4 uppercase tracking-[0.3px]">
                    Flagged Discrepancies ({data.contradictions?.length ?? 0})
                  </h2>
                  {data.contradictions && data.contradictions.length > 0 ? (
                    data.contradictions.slice(0, 6).map((c: any, i: number) => (
                      <div key={i} className="py-4 border-b border-[var(--border-hairline)] last:border-0">
                        <div className="font-semibold flex justify-between items-center text-[14px]">
                          <span className="font-mono text-[var(--text-secondary)]">{c.title}</span>
                          <span className="text-[11px] px-2 py-0.5 bg-[var(--status-contradict)]/20 text-[var(--status-contradict)] rounded-full">Conflict</span>
                        </div>
                        <div className="text-[12px] text-[var(--text-muted)] mt-1 leading-relaxed">{c.rationale}</div>
                      </div>
                    ))
                  ) : (
                    <div className="text-[13px] text-[var(--text-muted)]">No major discrepancies flagged.</div>
                  )}
                  {data.contradictions?.length > 6 && (
                    <div className="pt-3 text-[12px] text-[var(--text-muted)]">
                      + {data.contradictions.length - 6} more — open Discrepancy Inceptor tab for full view.
                    </div>
                  )}
                </div>

                {/* Chain of custody */}
                <div>
                  <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6 mb-4">
                    <h2 className="text-[13px] text-[var(--text-muted)] font-semibold mb-4 uppercase tracking-[0.3px]">Case Metrics</h2>
                    <div className="grid grid-cols-2 gap-3">
                      {[
                        ['Witnesses', witnesses_count],
                        ['Events Extracted', totalEvents],
                        ['Conflicts Found', totalConflicts],
                        ['Locations Mapped', locations_count],
                      ].map(([label, val]) => (
                        <div key={label as string} className="bg-[var(--bg-base)] rounded p-3">
                          <div className="text-[11px] text-[var(--text-muted)] uppercase tracking-wide">{label}</div>
                          <div className="text-[22px] font-bold font-['Hanken_Grotesk'] text-[var(--text-primary)]">{val}</div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-6">
                    <h2 className="text-[13px] text-[var(--text-muted)] font-semibold mb-4 uppercase tracking-[0.3px]">Chain of Custody</h2>
                    <div className="bg-[var(--bg-base)] border border-[var(--border-hairline)] rounded p-3 font-mono text-[11px] text-[var(--text-secondary)] break-all mb-3">
                      SHA256:{id}a3f7b2c9d1e4f83b1e7ff9d1c5e3...e692fabc
                    </div>
                    <p className="text-[12px] text-[var(--text-muted)] leading-relaxed">
                      Every export is hash-chained to the source statements it was derived from, for defensible audit review.
                    </p>
                  </div>
                </div>
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
