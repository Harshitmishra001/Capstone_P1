import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from ml_core.orchestrator import analyze_incident

app = FastAPI(
    title="Silent Witness API",
    description="Backend ML API for analyzing eyewitness testimonies",
    version="1.0.0"
)

class IncidentRequest(BaseModel):
    statements: List[str]

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Silent Witness Backend is running"}

@app.post("/analyze", response_model=Dict[str, Any])
def analyze_statements(req: IncidentRequest):
    if not req.statements:
        raise HTTPException(status_code=400, detail="Must provide at least one statement.")
        
    try:
        # Pass the raw text list directly to our newly built orchestrator
        results = analyze_incident(req.statements)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Standard local development runner
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
