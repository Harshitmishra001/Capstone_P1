import React, { useRef, useEffect, useState, useMemo } from 'react';
// @ts-ignore — react-force-graph-2d has no @types package
import ForceGraph2D from 'react-force-graph-2d';
import { Network, Maximize2, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const RelationshipGraph: React.FC<{ isFullScreen?: boolean; data?: any }> = ({ isFullScreen, data: rawData }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });
  const navigate = useNavigate();

  // Dynamically map graph data from ML output
  const data = useMemo(() => {
    if (!rawData || !rawData.raw_entities) {
      return { nodes: [], links: [] };
    }
    const nodesMap = new Map();
    const links: Array<{ source: string; target: string; type: string }> = [];
    
    // Create Witness nodes and Entity nodes
    rawData.raw_entities.forEach((ent: any) => {
      const stmtIdx = parseInt(ent.source_statement_id?.split('_')[1] || '0');
      const witnessId = `Witness ${String.fromCharCode(65 + stmtIdx)}`;
      
      // Ensure witness node exists
      if (!nodesMap.has(witnessId)) {
        nodesMap.set(witnessId, { id: witnessId, group: 1, val: 12 });
      }
      
      // Ensure entity node exists
      if (!nodesMap.has(ent.text)) {
        nodesMap.set(ent.text, { id: ent.text, group: 2, val: 8 });
      }
      
      // Link witness to entity they mentioned
      links.push({ source: witnessId, target: ent.text, type: 'mention' });
    });
    
    // Extract contradictions for red dotted edges
    if (rawData.contradictions) {
      rawData.contradictions.forEach((c: any) => {
        if (c.claims && c.claims.length >= 2) {
          links.push({ source: c.claims[0].witness, target: c.claims[1].witness, type: 'contradict' });
        }
      });
    }

    return {
      nodes: Array.from(nodesMap.values()),
      links: links
    };
  }, [rawData]);

  useEffect(() => {
    if (containerRef.current) {
      setDimensions({
        width: containerRef.current.clientWidth,
        height: containerRef.current.clientHeight - (isFullScreen ? 40 : 40)
      });
    }
    const handleResize = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.clientWidth,
          height: containerRef.current.clientHeight - 40
        });
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [isFullScreen]);

  const drawNode = (node: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
    const label = node.id;
    const fontSize = 12/globalScale;
    ctx.font = `${fontSize}px "IBM Plex Sans"`;
    
    ctx.beginPath();
    ctx.arc(node.x, node.y, node.val, 0, 2 * Math.PI, false);
    ctx.fillStyle = node.group === 1 ? '#4FA3E3' : '#1B1F26'; 
    ctx.fill();
    ctx.strokeStyle = '#2A2F38';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#E8EAED';
    ctx.fillText(label, node.x, node.y + node.val + 6);
  };

  const drawLink = (link: any, ctx: CanvasRenderingContext2D) => {
    ctx.beginPath();
    ctx.moveTo(link.source.x, link.source.y);
    ctx.lineTo(link.target.x, link.target.y);
    
    if (link.type === 'contradict') {
      ctx.strokeStyle = '#E3574F';
      ctx.setLineDash([4, 4]);
      ctx.lineWidth = 2;
    } else if (link.type === 'corroborate') {
      ctx.strokeStyle = '#3FB88A';
      ctx.setLineDash([]);
      ctx.lineWidth = 1.5;
    } else {
      ctx.strokeStyle = '#5B6472';
      ctx.setLineDash([]);
      ctx.lineWidth = 1;
    }
    
    ctx.stroke();
    ctx.setLineDash([]); 
  };

  return (
    <div className={`w-full flex flex-col bg-[var(--bg-base)] relative ${isFullScreen ? 'h-screen' : 'h-full border-r border-[var(--border-hairline)] shrink-0 max-w-[400px]'}`}>
      <div className="h-10 border-b border-[var(--border-hairline)] bg-[var(--bg-surface-2)] px-3 flex items-center justify-between shrink-0 absolute top-0 left-0 right-0 z-10">
        <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase tracking-wider flex items-center">
          {isFullScreen && (
            <button onClick={() => navigate(-1)} className="mr-3 text-[var(--text-secondary)] hover:text-[var(--text-primary)] cursor-pointer">
              <ArrowLeft className="w-4 h-4" />
            </button>
          )}
          <Network className="w-3.5 h-3.5 mr-2" />
          Relationship Graph
        </span>
        {!isFullScreen && (
          <button 
            onClick={() => navigate('graph')} 
            className="text-[var(--text-muted)] hover:text-[var(--text-primary)] transition p-1 hover:bg-[var(--bg-surface)] rounded cursor-pointer focus-bracket"
            title="Full Screen Graph"
          >
            <Maximize2 className="w-3.5 h-3.5" />
          </button>
        )}
      </div>
      <div ref={containerRef} className="flex-1 w-full pt-10">
        <ForceGraph2D
          width={dimensions.width}
          height={dimensions.height}
          graphData={data}
          nodeCanvasObject={drawNode}
          linkCanvasObjectMode={() => 'replace'}
          linkCanvasObject={drawLink}
          backgroundColor="#0B0D10"
          enableNodeDrag={true}
        />
      </div>
    </div>
  );
};
