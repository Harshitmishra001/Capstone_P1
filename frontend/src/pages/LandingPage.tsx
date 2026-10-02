import React from 'react';
import { useNavigate } from 'react-router-dom';

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-[var(--bg-base)] text-[var(--text-primary)] font-body">
      <nav className="flex items-center justify-between py-8 px-12 max-w-7xl mx-auto">
        <div className="font-[Archivo_Black] font-black text-[15px] tracking-[0.5px]">
          SILENT<span className="text-[var(--accent)] mx-0.5">·</span>WITNESS
        </div>
        <div className="flex gap-8 text-[var(--text-muted)] text-[13px] font-semibold">
          <a href="#" className="hover:text-[var(--text-primary)] transition">Product</a>
          <a href="#" className="hover:text-[var(--text-primary)] transition">Method</a>
          <a href="#" className="hover:text-[var(--text-primary)] transition">Ethics</a>
        </div>
        <div className="flex items-center gap-4">
          <button 
            onClick={() => navigate('/dashboard')}
            className="px-5 py-2.5 bg-white/5 border border-[var(--border-hairline)] text-[var(--text-primary)] font-bold text-[13px] rounded hover:bg-white/10 transition-colors"
          >
            Log in
          </button>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-12 py-24 grid md:grid-cols-[1.05fr_0.95fr] gap-16 items-center">
        <div>
          <div className="text-[var(--text-muted)] text-[13px] mb-4 max-w-[360px]">
            A reconstruction tool for journalists and legal reviewers
          </div>
          <h1 className="font-['Hanken_Grotesk'] font-extrabold text-[58px] leading-[1.05] tracking-[-1px] max-w-[560px] mb-8">
            Every witness saw an angle. Rarely the same one.
          </h1>
          <p className="text-[17px] text-[var(--text-secondary)] leading-[1.6] max-w-[440px] mb-10">
            Silent Witness reads multiple accounts of one incident, rebuilds them onto a shared timeline and map, and shows exactly where the stories align — and where they don't. It never decides who's right.
          </p>
          <div className="flex gap-4">
            <button 
              onClick={() => navigate('/incidents/SW-2024-0142')}
              className="px-[18px] py-[10px] bg-[var(--accent)] text-[var(--bg-base)] font-semibold text-[13px] rounded flex items-center hover:opacity-90 transition-opacity"
            >
              Open case dossier
            </button>
            <button 
              onClick={() => navigate('/dashboard')}
              className="px-[18px] py-[10px] bg-white/5 border border-[var(--border-hairline)] text-[var(--text-primary)] font-semibold text-[13px] rounded hover:bg-white/10 transition-colors"
            >
              See all cases
            </button>
          </div>
          <div className="mt-6 text-[13px] text-[var(--text-muted)]">
            Non-adjudicative by design — findings are traceable, not scored.
          </div>
        </div>

        <div className="relative h-[480px]">
          <div className="absolute top-0 left-0 w-[180px] bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-4 text-[13px] text-[var(--text-secondary)] leading-[1.55]">
            <div className="font-mono text-[12px] text-[var(--text-muted)] mb-2">Witness A · 06:42pm</div>
            Sedan was red, turning left onto 9th.
          </div>
          
          <div className="absolute top-[110px] right-0 w-[180px] bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-4 text-[13px] text-[var(--text-secondary)] leading-[1.55]">
            <div className="font-mono text-[12px] text-[var(--text-muted)] mb-2">Witness B · 06:43pm</div>
            Dark car, maybe grey, went straight through.
          </div>
          
          <div className="absolute top-[230px] left-[70px] w-[180px] bg-[var(--bg-surface)] border border-[var(--border-hairline)] rounded-lg p-4 text-[13px] text-[var(--text-secondary)] leading-[1.55]">
            <div className="font-mono text-[12px] text-[var(--text-muted)] mb-2">Witness C · 06:42pm</div>
            Confirms red vehicle, turning left.
          </div>

          <div className="absolute top-[355px] left-0 flex items-center gap-2 px-3.5 py-[7px] bg-[var(--status-corroborate)]/20 text-[var(--status-corroborate)] rounded-full text-[12px] font-bold whitespace-nowrap">
            <span className="w-1.5 h-1.5 rounded-full bg-current"></span>
            2 witnesses agree — colour
          </div>
          
          <div className="absolute bottom-0 right-0 flex items-center gap-2 px-3.5 py-[7px] bg-[var(--status-contradict)]/20 text-[var(--status-contradict)] rounded-full text-[12px] font-bold whitespace-nowrap">
            <span className="w-1.5 h-1.5 rounded-full bg-current"></span>
            Direction of travel conflicts
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-12 pb-24">
        <div className="grid md:grid-cols-3 border-t border-[var(--border-hairline)]">
          <div className="pr-6 py-8 border-r border-[var(--border-hairline)]">
            <h3 className="font-['Hanken_Grotesk'] font-bold text-[17px] mb-2">Ingest freely written statements</h3>
            <p className="text-[13px] text-[var(--text-muted)] leading-[1.6]">Paste or bulk-upload accounts as given — no rigid intake form. Entities, times and places are extracted automatically.</p>
          </div>
          <div className="px-6 py-8 border-r border-[var(--border-hairline)]">
            <h3 className="font-['Hanken_Grotesk'] font-bold text-[17px] mb-2">Reconstruct one shared account</h3>
            <p className="text-[13px] text-[var(--text-muted)] leading-[1.6]">Claims from every witness align onto a single timeline and map, so overlapping and diverging details sit side by side.</p>
          </div>
          <div className="pl-6 py-8">
            <h3 className="font-['Hanken_Grotesk'] font-bold text-[17px] mb-2">Trace every flag to its source</h3>
            <p className="text-[13px] text-[var(--text-muted)] leading-[1.6]">Click any agreement or contradiction and land on the exact sentence it came from. No claim without a citation.</p>
          </div>
        </div>
      </div>
    </div>
  );
};
