import React, { useEffect, useRef } from 'react';
import { Timeline } from 'vis-timeline/standalone';
import { DataSet } from 'vis-data';
import 'vis-timeline/styles/vis-timeline-graph2d.min.css';
import type { TimelineItem } from '../types';
import { Maximize2, ZoomIn, ZoomOut } from 'lucide-react';

export const TemporalView: React.FC<{ items: TimelineItem[], setFocusedEntityId?: (id: string) => void }> = ({ items, setFocusedEntityId }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const timelineRef = useRef<Timeline | null>(null);

  useEffect(() => {
    if (!containerRef.current || items.length === 0) return;
    
    const witnesses = Array.from(new Set(items.map(i => i.witness)));
    
    const groups = new DataSet(witnesses.map((w) => ({
      id: w, 
      content: `<div class="font-ui font-semibold text-[var(--text-primary)] text-sm flex items-center h-full px-2"><div class="w-6 h-6 rounded bg-[var(--bg-surface-2)] border border-[var(--border-hairline)] flex items-center justify-center mr-2 text-xs font-mono text-[var(--text-secondary)]">${w.charAt(0)}</div>${w}</div>`,
      className: 'vis-group-custom'
    })));

    const dataset = new DataSet(items.map(item => ({
      id: item.id,
      content: `<div class="font-body text-xs whitespace-normal line-clamp-2 px-1" title="${item.content}">${item.content}</div>`,
      start: item.start,
      group: item.witness,
      className: 'bg-[var(--bg-surface-2)] border-[var(--border-hairline)] text-[var(--text-primary)] hover:border-[var(--accent)] transition-colors'
    })));

    const options = {
      stack: false,
      zoomMin: 1000 * 60,
      zoomMax: 1000 * 60 * 60 * 24,
      margin: { item: 10, axis: 5 },
      format: {
        minorLabels: { minute: 'h:mma', hour: 'ha' }
      },
      orientation: 'top',
      groupHeightMode: 'fixed'
    };

    timelineRef.current = new Timeline(containerRef.current, dataset, groups, options as any);
    
    timelineRef.current.on('select', (props) => {
      if (props.items.length > 0 && setFocusedEntityId) {
        setFocusedEntityId(props.items[0]);
      }
    });

    return () => {
      if (timelineRef.current) timelineRef.current.destroy();
    };
  }, [items, setFocusedEntityId]);

  return (
    <div className="h-48 w-full flex flex-col relative bg-[var(--bg-base)] border-b border-[var(--border-hairline)] shrink-0">
      <div className="h-8 bg-[var(--bg-surface-2)] border-b border-[var(--border-hairline)] px-3 flex items-center justify-between shrink-0">
        <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase tracking-wider">Temporal Sequence (Swimlanes)</span>
        <div className="flex space-x-1">
          <button className="text-[var(--text-muted)] hover:text-[var(--text-primary)] transition p-1 hover:bg-[var(--bg-surface)] rounded cursor-pointer focus-bracket"><ZoomIn className="w-3.5 h-3.5" /></button>
          <button className="text-[var(--text-muted)] hover:text-[var(--text-primary)] transition p-1 hover:bg-[var(--bg-surface)] rounded cursor-pointer focus-bracket"><ZoomOut className="w-3.5 h-3.5" /></button>
          <button className="text-[var(--text-muted)] hover:text-[var(--text-primary)] transition p-1 hover:bg-[var(--bg-surface)] rounded cursor-pointer focus-bracket"><Maximize2 className="w-3.5 h-3.5" /></button>
        </div>
      </div>
      <div className="flex-1 relative">
         <div ref={containerRef} className="absolute inset-0 custom-vis-timeline overflow-hidden"></div>
         {/* Fake SVG Arc for demo purposes. */}
         <svg className="absolute inset-0 pointer-events-none z-10 w-full h-full">
            <path d="M 300,50 Q 400,90 500,130" className="arc-contradict" />
         </svg>
      </div>
    </div>
  );
};
