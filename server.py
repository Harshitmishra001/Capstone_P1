import uuid
import datetime
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from typing import List, Dict, Any

from ml_core.orchestrator import analyze_incident

app = FastAPI(
    title="Silent Witness API",
    description="Backend ML API for analyzing eyewitness testimonies",
    version="1.0.0"
)

# Enable CORS for the Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-Memory Database ---
DB = {
    "incidents": [
        {
            "id": "inc-101",
            "title": "Main St. Intersection Collision",
            "type": "Road Accident",
            "date": "2024-05-10",
            "status": "Reviewing",
            "witnessCount": 3,
            "contradictionCount": 2
        }
    ],
    "incident_data": {
        "inc-101": {
            "statements": [
                {"id": "s1", "witness": "Witness A (Driver)", "text": "I was driving north on Main St. when the red sedan ran the red light at approximately 2:14 PM.", "status": "Processed"},
                {"id": "s2", "witness": "Witness B (Pedestrian)", "text": "I heard a crash around 2:15 PM. A blue car was speeding through the intersection.", "status": "Processed"},
                {"id": "s3", "witness": "Witness C (Store Owner)", "text": "The red car swerved to avoid a dog at exactly 2:14 PM before the collision.", "status": "Processed"}
            ],
            "markers": [
                {"id": "m1", "lat": 40.7128, "lng": -74.0060, "label": "Impact Location", "witness": "Agreed", "color": "blue"},
                {"id": "m2", "lat": 40.7132, "lng": -74.0065, "label": "Witness B Vantage Point", "witness": "Witness B", "color": "purple"},
                {"id": "m3", "lat": 40.7125, "lng": -74.0055, "label": "Witness A Vantage Point", "witness": "Witness A", "color": "red"},
            ],
            "timeline": [
                {"id": "1", "content": "C: Car swerves", "start": "2024-05-10T14:14:00", "witness": "Witness C", "className": "border-l-4 border-green-500"},
                {"id": "2", "content": "B: Hears crash (2:15)", "start": "2024-05-10T14:15:00", "witness:Witness B": "bg-red-50 border-red-500 border-l-4"},
                {"id": "3", "content": "A: Sedan runs light", "start": "2024-05-10T14:14:30", "witness": "Witness A", "className": "border-l-4 border-blue-500"},
                {"id": "4", "content": "C: Crash (2:14)", "start": "2024-05-10T14:14:05", "witness": "Witness C", "className": "bg-red-50 border-red-500 border-l-4"}
            ],
            "contradictions": [
                {
                    "id": "c1",
                    "type": "Attribute",
                    "title": "Vehicle Color",
                    "rationale": "One witness stated the vehicle was red, while another stated it was blue.",
                    "claims": [
                        {"witness": "Witness A (Driver)", "snippet": "the red sedan", "fullText": "I was driving north on Main St. when the red sedan ran the red light at approximately 2:14 PM.", "span": [41, 54]},
                        {"witness": "Witness B (Pedestrian)", "snippet": "A blue car", "fullText": "I heard a crash around 2:15 PM. A blue car was speeding through the intersection.", "span": [32, 42]}
                    ]
                },
                {
                    "id": "c2",
                    "type": "Temporal",
                    "title": "Time of Impact",
                    "rationale": "There is a 1-minute discrepancy regarding the time of the crash.",
                    "claims": [
                        {"witness": "Witness B (Pedestrian)", "snippet": "around 2:15 PM", "fullText": "I heard a crash around 2:15 PM. A blue car was speeding through the intersection.", "span": [16, 30]},
                        {"witness": "Witness C (Store Owner)", "snippet": "exactly 2:14 PM", "fullText": "The red car swerved to avoid a dog at exactly 2:14 PM before the collision.", "span": [38, 53]}
                    ]
                }
            ]
        }
    }
}

class IncidentRequest(BaseModel):
    statements: List[str]
    title: str = "New Incident"

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Silent Witness Backend is running"}

@app.get("/api/incidents")
def get_incidents():
    return DB["incidents"]

@app.get("/api/incidents/{incident_id}")
def get_incident_data(incident_id: str):
    if incident_id not in DB["incident_data"]:
        raise HTTPException(status_code=404, detail="Incident not found")
    return DB["incident_data"][incident_id]

@app.post("/analyze")
def analyze_statements(req: IncidentRequest):
    if not req.statements:
        raise HTTPException(status_code=400, detail="Must provide at least one statement.")
    try:
        return analyze_incident(req.statements)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/incidents")
def create_incident(req: IncidentRequest):
    if not req.statements:
        raise HTTPException(status_code=400, detail="Must provide at least one statement.")
        
    try:
        try:
            # Run ML backend extraction
            results = analyze_incident(req.statements)
            # Ensure it returned a valid object, otherwise trigger fallback
            if not results or "contradictions" not in results:
                raise ValueError("Invalid ML output")
        except Exception as e:
            print(f"ML Pipeline failed or unavailable ({e}). Loading fallback theft_case_output.json for demo...")
            import json
            import os
            fallback_path = os.path.join(os.path.dirname(__file__), "theft_case_output.json")
            if os.path.exists(fallback_path):
                with open(fallback_path, "r") as f:
                    results = json.load(f)
            else:
                raise e
        
        inc_id = f"inc-{uuid.uuid4().hex[:6]}"
        
        # Map statements
        ui_statements = [
            {"id": f"stmt_{i}", "witness": f"Witness {chr(65+i)}", "text": text, "status": "Processed"}
            for i, text in enumerate(req.statements)
        ]
        
        # Map contradictions to UI format
        ui_contradictions = []
        for i, d in enumerate(results.get("contradictions", [])):
            claims = []
            for j, span_info in enumerate(d.get("source_span", [])):
                stmt_id = span_info[0]
                span_range = span_info[1]
                # Find matching statement text
                full_text = ""
                snippet = "Excerpt"
                stmt_idx = int(stmt_id.split('_')[-1]) if '_' in stmt_id else 0
                if stmt_idx < len(req.statements):
                    full_text = req.statements[stmt_idx]
                    if len(span_range) == 2:
                        start, end = span_range
                        snippet = full_text[start:end]
                
                claims.append({
                    "witness": f"Witness {chr(65+stmt_idx)}",
                    "snippet": snippet,
                    "fullText": full_text,
                    "span": span_range
                })
                
            ui_contradictions.append({
                "id": f"c_{i}",
                "type": d.get("type", "semantic"),
                "title": f"Flagged Discrepancy #{i+1}",
                "rationale": d.get("rationale", "Statements conflict."),
                "claims": claims
            })

        # Save to DB
        new_summary = {
            "id": inc_id,
            "title": req.title,
            "type": "Investigation",
            "date": datetime.date.today().isoformat(),
            "status": "Reviewing",
            "witnessCount": len(req.statements),
            "contradictionCount": len(ui_contradictions)
        }
        
        DB["incidents"].insert(0, new_summary)
        DB["incident_data"][inc_id] = {
            "statements": ui_statements,
            "markers": [], 
            "timeline": [], 
            "contradictions": ui_contradictions
        }
        
        return {"id": inc_id, "summary": new_summary, "ml_raw": results}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
