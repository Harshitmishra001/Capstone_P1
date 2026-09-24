# Silent Witness - Project Summary & Workflow

> **Notice:** This file serves as the **Single Source of Truth** for the project's architecture, ML flow, and backend-frontend integrations. As the codebase evolves through multi-collaborator git pulls, all structural and workflow logic changes must be updated here first.

---

## 1. Machine Learning (ML) Core Flow
The NLP/ML logic is self-contained within the `ml_core/` package and is triggered end-to-end via the `analyze_incident()` orchestrator.

### Processing Pipeline
1. **Data Ingestion:**
   - Raw text statements are passed to the orchestrator.
   - Converted into internal `Statement` objects (from `ml_core.schema.models`).
2. **Local Deterministic Extraction (Intra-Document):**
   - **NER (`extract_entities`)**: SpaCy-based named entity recognition.
   - **Temporal & Spatial (`extract_temporal_references`, `extract_spatial_references`)**: Regex and dependency parsing to find location/time markers.
   - **Coref Resolution (`resolve_single_document_coref`)**: Pronoun clustering using `fastcoref` (or fallback).
3. **LLM Semantic Extraction:**
   - **Events (`extract_events_llm`)**: LLM (e.g. SmolLM via LM Studio API) extracts structured `EventTuple` and `EventOccurrence` claims from the statement.
   - **Negation (`apply_negation_scoping`)**: Checks parse trees to flag negated events (e.g., "did not see the car").
4. **Cross-Document Alignment:**
   - **Cross-Coref (`resolve_cross_statement_coref`)**: Merges overlapping entities across multiple witness statements (e.g., matching "the red car" in Statement A with "the sedan" in Statement B).
   - **Claim Clustering (`align_claims`)**: Groups related semantic claims into clusters to analyze them against each other.
5. **Contradiction Detection:**
   - **Rule-based & NLI (`run_detection_pipeline`)**: Evaluates aligned events for attribute/temporal/spatial mismatches. Utilizes Isotonic Regression for calibration and triggers LLM rationale generation.
   - **Constraint**: *Never implies a witness is lying, only surfaces factual mismatch.*

---

## 2. Backend Architecture (`server.py`)
The backend is a FastAPI application serving the ML predictions to the frontend.

### Existing Endpoints
- `GET /`
  - **Purpose:** Health check.
  - **Returns:** `{"status": "ok", "message": "Silent Witness Backend is running"}`
  
- `POST /analyze`
  - **Purpose:** Processes a list of raw string testimonies through the ML pipeline.
  - **Input Payload:**
    ```json
    {
      "statements": [
        "I saw a red car speed through the intersection.",
        "The blue sedan did not stop at the light."
      ]
    }
    ```
  - **Returns:** `Dict[str, Any]` containing `metrics`, `entities`, `events`, and `contradictions` (formatted from `DetectionResult`).

---

## 3. Frontend-Backend Integration (Current & Future State)
Currently, the Vite/React frontend uses local Mock Data (`frontend/src/api/client.ts`). The goal is to fully wire these mock endpoints to the live `server.py` backend.

### Future Function Calls & Endpoints (Planned API Interface)
*Note: These signatures are subject to change as the graph visualization and authentication phases begin. Update this section if API schemas change.*

1. **`fetchIncidents()` -> `GET /api/incidents`**
   - **Frontend UI:** Dashboard list of cases.
   - **Backend Need:** Retrieve a lightweight list of all processed incidents (ID, title, date, witness count, flag count) from a database.

2. **`createIncident(data)` -> `POST /api/incidents`**
   - **Frontend UI:** "New Incident" button on Dashboard -> Ingestion Panel.
   - **Backend Need:** Creates a new container in the database.

3. **`processStatements(incident_id, statements)` -> `POST /api/incidents/{id}/analyze`**
   - **Frontend UI:** Clicking "Extract & Align" in the `IngestionPanel`.
   - **Backend Need:** This will wrap the current `POST /analyze` logic. The frontend will send the list of raw text, the backend runs `orchestrator.analyze_incident()`, saves results to DB, and returns the response.

4. **`fetchIncidentData(incident_id)` -> `GET /api/incidents/{id}/data`**
   - **Frontend UI:** Loading the `IncidentWorkspace` (Map, Timeline, Contradictions).
   - **Backend Need:** Returns the full processed JSON graph for the frontend to render:
     - `statements`: Array of statements for the sidebar.
     - `markers`: Array of spatial entities for the Leaflet map.
     - `timeline`: Array of temporal events for Vis-Timeline.
     - `contradictions`: Array of mismatches for the Analysis Panel (must contain `span` data for the Traceability Modal).

5. **`submitFeedback(flag_id, feedback)` -> `POST /api/feedback`**
   - **Frontend UI:** "Acknowledge" or "Flag for Review" on a contradiction.
   - **Backend Need:** Appends to the human-in-the-loop ML `feedback.jsonl` log.

---

## 4. How to Use This Document
If you fetch new code (`git pull`) that changes ML internal logic (e.g., adding a new contradiction type), database schemas, or FastAPI endpoint URLs:
1. Come here first and update the relevant section.
2. Only after updating this document should you modify the React API client (`frontend/src/api/client.ts`) or `server.py` to match.
