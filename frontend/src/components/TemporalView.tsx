import React, { useEffect, useRef } from 'react';
import { Timeline } from 'vis-timeline/standalone';
import { DataSet } from 'vis-data';
import 'vis-timeline/styles/vis-timeline-graph2d.min.css';
import type { TimelineItem } from '../types';
import { Maximize2, ZoomIn, ZoomOut } from 'lucide-react';

export const TemporalView: React.FC<{ items: TimelineItem[] }> = ({ items }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const timelineRef = useRef<Timeline | null>(null);

  useEffect(() => {
    if (!containerRef.current || items.length === 0) return;
    
    const dataset = new DataSet(items.map(item => ({
      id: item.id,
      content: item.content,
      start: item.start,
      className: item.className || 'border-l-4 border-blue-500',
      group: item.witness
    })));
    
    const groups = new DataSet([
      { id: "Witness A", content: "Witness A" },
      { id: "Witness B", content: "Witness B" },
      { id: "Witness C", content: "Witness C" }
    ]);

    const options = {
      stack: false,
      zoomMin: 1000 * 60,
      zoomMax: 1000 * 60 * 60 * 24,
      margin: { item: 10, axis: 5 },
      format: {
        minorLabels: { minute: 'h:mma', hour: 'ha' }
      }
    };

    timelineRef.current = new Timeline(containerRef.current, dataset, groups, options);
    
    return () => {
      if (timelineRef.current) {
        timelineRef.current.destroy();
      }
    };
  }, [items]);

  return (
    <div className="h-full w-full flex flex-col relative bg-white">
      <div className="h-10 border-b border-gray-200 bg-gray-50/80 px-3 flex items-center justify-between z-10 shrink-0">
        <span className="text-xs font-bold text-gray-600 uppercase tracking-wider">Timeline</span>
        <div className="flex space-x-2">
          <button className="text-gray-400 hover:text-gray-700 transition p-1 hover:bg-gray-200 rounded"><ZoomIn className="w-4 h-4" /></button>
          <button className="text-gray-400 hover:text-gray-700 transition p-1 hover:bg-gray-200 rounded"><ZoomOut className="w-4 h-4" /></button>
          <button className="text-gray-400 hover:text-gray-700 transition p-1 hover:bg-gray-200 rounded"><Maximize2 className="w-4 h-4" /></button>
        </div>
      </div>
      <div ref={containerRef} className="flex-1 w-full pt-4 px-4 pb-4 overflow-hidden z-0"></div>
    </div>
  );
};
