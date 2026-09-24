import type { IncidentSummary, Statement, MapMarker, TimelineItem, Contradiction } from '../types';

export const mockIncidents: IncidentSummary[] = [
  { id: "inc-101", title: "Main St. Intersection Collision", type: "Road Accident", date: "2024-05-10", status: "Reviewing", witnessCount: 3, contradictionCount: 2 },
  { id: "inc-102", title: "Downtown Convenience Store Robbery", type: "Robbery", date: "2024-05-08", status: "Active", witnessCount: 5, contradictionCount: 4 },
  { id: "inc-103", title: "Warehouse Fire Incident", type: "Fire", date: "2024-04-22", status: "Archived", witnessCount: 2, contradictionCount: 0 },
];

export const mockStatements: Statement[] = [
  { id: "s1", witness: "Witness A (Driver)", text: "I was driving north on Main St. when the red sedan ran the red light at approximately 2:14 PM.", status: "Processed" },
  { id: "s2", witness: "Witness B (Pedestrian)", text: "I heard a crash around 2:15 PM. A blue car was speeding through the intersection.", status: "Processed" },
  { id: "s3", witness: "Witness C (Store Owner)", text: "The red car swerved to avoid a dog at exactly 2:14 PM before the collision.", status: "Processed" }
];

export const mockMarkers: MapMarker[] = [
  { id: "m1", lat: 40.7128, lng: -74.0060, label: "Impact Location", witness: "Agreed", color: "blue" },
  { id: "m2", lat: 40.7132, lng: -74.0065, label: "Witness B Vantage Point", witness: "Witness B", color: "purple" },
  { id: "m3", lat: 40.7125, lng: -74.0055, label: "Witness A Vantage Point", witness: "Witness A", color: "red" },
];

export const mockTimeline: TimelineItem[] = [
  { id: "1", content: "C: Car swerves", start: "2024-05-10T14:14:00", witness: "Witness C", className: "border-l-4 border-green-500" },
  { id: "2", content: "B: Hears crash (2:15)", start: "2024-05-10T14:15:00", witness: "Witness B", className: "bg-red-50 border-red-500 border-l-4" },
  { id: "3", content: "A: Sedan runs light", start: "2024-05-10T14:14:30", witness: "Witness A", className: "border-l-4 border-blue-500" },
  { id: "4", content: "C: Crash (2:14)", start: "2024-05-10T14:14:05", witness: "Witness C", className: "bg-red-50 border-red-500 border-l-4" }
];

export const mockContradictions: Contradiction[] = [
  {
    id: "c1",
    type: "Attribute",
    title: "Vehicle Color",
    rationale: "One witness stated the vehicle was red, while another stated it was blue.",
    claims: [
      { witness: "Witness A (Driver)", snippet: "the red sedan", fullText: "I was driving north on Main St. when the red sedan ran the red light at approximately 2:14 PM.", span: [41, 54] },
      { witness: "Witness B (Pedestrian)", snippet: "A blue car", fullText: "I heard a crash around 2:15 PM. A blue car was speeding through the intersection.", span: [32, 42] }
    ]
  },
  {
    id: "c2",
    type: "Temporal",
    title: "Time of Impact",
    rationale: "There is a 1-minute discrepancy regarding the time of the crash.",
    claims: [
      { witness: "Witness B (Pedestrian)", snippet: "around 2:15 PM", fullText: "I heard a crash around 2:15 PM. A blue car was speeding through the intersection.", span: [16, 30] },
      { witness: "Witness C (Store Owner)", snippet: "exactly 2:14 PM", fullText: "The red car swerved to avoid a dog at exactly 2:14 PM before the collision.", span: [38, 53] }
    ]
  }
];

export const getIncidents = async () => {
  return mockIncidents;
};

export const getIncidentData = async (id?: string) => {
  return {
    statements: mockStatements,
    markers: mockMarkers,
    timeline: mockTimeline,
    contradictions: mockContradictions
  };
};
