# Audit Report: Silent Witness (Capstone_P1)

## Summary
The codebase has undergone a comprehensive multi-stage audit and remediation. All critical and high-priority discrepancies between claims and implementation—including frontend build failures, fake delays, merge conflict artifacts, untracked/bloated mock state, orphaned feedback modules, and heuristic comparator bugs—have been systematically resolved.

- **Frontend Status:** **PASS** (`npm run build` succeeds with 0 TypeScript errors).
- **Backend & ML Core Status:** **PASS** (Full unit and integration test suite passing: 26 tests across spatial resolution, isotonic calibration, negation overrides, coreference resolution, and FastAPI server endpoints).
- **Storage & Architecture:** Clean SQLite persistence with seed data decoupled from `server.py` into `seed_data.py` (~93% reduction in `server.py` size).
- **Human-in-the-Loop Feedback:** Live `POST /api/feedback` backend endpoint connected to investigator review UI buttons in Discrepancy Inceptor.

---

## Claims vs Reality (Post-Audit Resolution)

| Feature | Claimed Where | Status | Evidence & Resolution |
|---|---|---|---|
| **Frontend Production Build** | `README.md:5, 217` | **RESOLVED** | TypeScript compilation errors in `RelationshipGraph.tsx` and `IncidentWorkspace.tsx` resolved; `npm run build` builds cleanly to `frontend/dist/`. |
| **Semantic Vector Clustering** | `README.md:133-136` | **VERIFIED** | `ml_core/alignment/cluster.py:35-46` encodes using `all-MiniLM-L6-v2` and runs `AgglomerativeClustering`. Verified operational. |
| **Local LLM Event Extraction** | `README.md:127-130` | **VERIFIED** | `ml_core/extraction/events.py` calls local OpenAI-compatible endpoint (LM Studio), parses and validates Pydantic event tuples. |
| **Synthetic Forensic Dataset** | `README.md:193-205` | **VERIFIED** | `ml_core/synthetic/transcripts/` contains 20 scenarios with 400 long-form testimonies; `generated/` contains 100 incident JSON files. |
| **Interactive Spatial Map** | `README.md:48, 71` | **RESOLVED** | Offline deterministic landmark coordinate resolution table in `spatial.py` resolves locations locally without external API dependencies; mapped to Leaflet map markers. |
| **Chronological Timeline** | `README.md:48, 70` | **RESOLVED** | Real extracted temporal references from `orchestrator.py` (`all_temporals`) are mapped to Vis-Timeline items. |
| **Cross-Statement Coreference** | `project_summary.md:22` | **RESOLVED** | Entity attribute extraction (color, vehicle make, person roles) populated in `ner.py`; cross-statement named-entity matching implemented in `coref.py` with unit tests in `test_coref.py`. |
| **Negation Contradiction Override** | `README.md:123` | **RESOLVED** | `evaluate_negation_override` in `rules.py` enforces action compatibility, object overlap, and subject identity constraints before declaring contradictions. |
| **Spatio-Temporal Extraction** | `README.md:120-122` | **RESOLVED** | `orchestrator.py` aggregates `all_temporals` and `all_spatials`, attaches spatial/temporal anchors to extracted events, and returns them in the output graph. |
| **Confidence Calibration** | `project_summary.md:25`, `IncidentWorkspace.tsx:313` | **RESOLVED** | `ConfidenceCalibrator` initialized with empirical isotonic baseline curve (`fit_baseline=True`); verified monotonic in `test_pipeline.py`. Likelihood bar dynamically reflects model confidence. |
| **Quantitative Pipeline Evaluation** | `README.md:402`, `capstone_report.tex:1022` | **RESOLVED** | `ml_core/tests/eval_pipeline.py` runs evaluation on benchmark incident datasets in `ml_core/synthetic/generated/` and generates empirical `ml_core/eval_report.md`. |
| **Testimony Ingestion Drawer** | `README.md:69`, `IngestionDrawer.tsx` | **RESOLVED** | Fake 4-second timeout removed; form submission triggers statement extraction directly via backend. |
| **Evidentiary Dossier & Custody Hash** | `IncidentWorkspace.tsx:345-360` | **RESOLVED** | Real export functions for Dossier (`.txt`), Claim Graph (`.json`), and CSV (`.csv`); live SHA-256 chain of custody computed using Web Crypto API. |
| **Global Command Bar (Ctrl+K)** | `frontend/src/components/CommandBar.tsx` | **RESOLVED** | Connected to live incidents API via `getIncidents()`; supports keyboard navigation and dynamic incident selection. |
| **Human-in-the-loop Feedback** | `README.md:417`, `project_summary.md:79` | **RESOLVED** | Live `POST /api/feedback` endpoint in `server.py` recording to `feedback_log.jsonl`; UI review buttons added in `IncidentWorkspace.tsx`. |
| **Persistent Storage** | `project_summary.md:61-65` | **RESOLVED** | SQLite database (`silent_witness.db`) persists incidents across server restarts; 4,800 lines of mock JSON decoupled to `seed_data.py`. |
| **Configured Local LLM URL** | `README.md:303` | **RESOLVED** | `ml_core/llm_client.py` checks both `LOCAL_LLM_URL` and `LM_STUDIO_URL`, defaulting to standard `http://127.0.0.1:1234/v1`. |

---

## Issues by Severity (Remediation Summary)

### Critical (All Resolved)
1. **Frontend Production Build Failure:** Fixed TypeScript variable types (`links` typing) and removed unused declarations in `RelationshipGraph.tsx` and `IncidentWorkspace.tsx`. `npm run build` exits 0.
2. **Silent Statement Replacement on Fallback:** Fixed in `server.py`. When fallback is utilized, user statements are preserved, spans are clamped within bounds, and UI explicitly displays `Demo (Fallback)` status badge.
3. **Unchecked Negation Contradiction Logic:** Fixed in `ml_core/detection/rules.py`. Verifies subject, action compatibility, and object overlap before returning contradiction status.

### High (All Resolved)
4. **Hardcoded Spatial Coordinates & Sequential Timestamps:** Added offline landmark coordinate geocoding in `spatial.py` and real temporal reference mapping in `server.py`.
5. **Fabricated Evaluation Metrics:** Replaced fake constants with empirical benchmark evaluation script `eval_pipeline.py` running against 100 benchmark incidents.
6. **Broken Cross-Statement Coreference:** Entity attribute extraction implemented in `ner.py`; cross-statement matching logic enhanced in `coref.py`.
7. **Discarded Spatio-Temporal Extractions:** `orchestrator.py` wires `spatials` and `temporals` into the returned dictionary.

### Medium (All Resolved)
8. **Fake Ingestion Drawer UX:** Removed artificial timer; connected drawer directly to incident creation.
9. **Fake Evidentiary Dossier & Custody Hash:** Real text dossier, CSV, and graph exports implemented; dynamic SHA-256 hash computed over incident data.
10. **Hardcoded Global Command Bar:** Dynamic lookup querying active incidents list in `CommandBar.tsx`.
11. **Environment Variable Inconsistency:** Standardized on `LOCAL_LLM_URL` / `LM_STUDIO_URL` in `llm_client.py`.
12. **Monolithic In-Memory Mock Database:** Moved static JSON out of `server.py` into `seed_data.py`, initialized SQLite backing.
13. **Weak Test Suite Coverage:** Expanded from 12 basic tests to 26 comprehensive unit and integration tests.

### Low (All Resolved)
14. **Compiled Bytecode Tracked in Git:** Verified no `.pyc` files are tracked; `.gitignore` rules active.
15. **Hardcoded User Path in Test Script:** Portable `os.path.dirname(__file__)` paths in `test_mapping.py`.
16. **Swallowed Exceptions:** Removed silent `pass` blocks in `coref.py` and `orchestrator.py`, replacing with structured logging.
17. **Dead Scratch Files:** Cleaned up unused root-level scratch scripts (`inject_seed.py`, `generate_seed.py`).

---

## Verification Evidence

### 1. Pytest Test Suite (`ml_core/tests/`)
- Command: `python -m pytest ml_core/tests/ -v`
- Result: **26 passed in 37.14s (0 failures, 0 errors)**
- Test modules covered:
  - `test_spatial.py`: 3 passed (offline landmark coordinate resolution)
  - `test_pipeline.py`: 4 passed (guardrails, isotonic calibration curve)
  - `test_negation.py`: 8 passed (negation override heuristics and rules)
  - `test_coref.py`: 3 passed (intra-document and cross-statement named entity coreference)
  - `test_orchestrator_integration.py`: 5 passed (FastAPI routes, pipeline execution, feedback logging)
  - `test_events.py`: 3 passed (event extraction and validation)

### 2. Frontend Production Build (`frontend/`)
- Command: `npm run build` (`tsc -b && vite build`)
- Result: **SUCCESS (Exit Code 0)**
- Artifacts generated:
  - `dist/index.html` (0.87 kB)
  - `dist/assets/index-*.css` (64.59 kB)
  - `dist/assets/index-*.js` (1,328.56 kB)
