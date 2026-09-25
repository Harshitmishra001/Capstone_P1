export interface IncidentSummary {
  id: string;
  title: string;
  type: string;
  date: string;
  status: "Active" | "Archived" | "Reviewing";
  witnessCount: number;
  contradictionCount: number;
}

export interface Statement {
  id: string;
  witness: string;
  text: string;
  status: "Processing" | "Processed";
}

export interface MapMarker {
  id: string;
  lat: number;
  lng: number;
  label: string;
  witness: string;
  color: string;
}

export interface TimelineItem {
  id: string;
  content: string;
  start: string;
  witness: string;
  className?: string;
}

export interface Contradiction {
  id: string;
  type: string;
  title: string;
  rationale: string;
  claims: {
    witness: string;
    snippet: string;
    fullText: string;
    span: [number, number];
  }[];
}
