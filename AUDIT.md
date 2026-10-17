# Audit Report: Silent Witness (Capstone_P1)

## Summary
Roughly **40–45% working prototype**. The deterministic NLP tagging (spaCy), vector claim clustering (`all-MiniLM-L6-v2`), local LLM event extraction, and raw synthetic testimonies are real and operational. However, the frontend **fails to build** due to 5 TypeScript errors; the spatial map and chronological timeline use **hardcoded/simulated coordinates and timestamps**; isotonic calibration and evaluation metrics in `eval_report.md` are **completely fabricated**; the coreference resolution is non-functional because extracted entity attributes are always empty; and several UI features (Ingestion Drawer extraction, Evidentiary Dossier exports, CommandBar search) are purely simulated mockups.

---

## Claims vs Reality

| Feature | Claimed Where | Status | Evidence |
|---|---|---|---|
| **Frontend Production Build** | `README.md:5, 217` | **BROKEN** | `npm run build` fails with 5 TypeScript errors (`RelationshipGraph.tsx:17, 49`, `IncidentWorkspace.tsx:48, 225`). |
| **Semantic Vector Clustering** | `README.md:133-136` | **REAL** | `ml_core/alignment/cluster.py:35-46` encodes using `all-MiniLM-L6-v2` and runs `AgglomerativeClustering`. Verified working. |
| **Local LLM Event Extraction** | `README.md:127-130` | **REAL** | `ml_core/extraction/events.py:17-90` calls local OpenAI-compatible endpoint (LM Studio), parses and validates Pydantic event tuples. |
| **Synthetic Forensic Dataset** | `README.md:193-205` | **REAL** | `ml_core/synthetic/transcripts/` contains 20 scenarios with 400 long-form testimonies; `generated/` contains 100 incident JSON files. |
| **Interactive Spatial Map** | `README.md:48, 71` | **FAKE** | `server.py:5018-5030` hardcodes New York coordinates `(40.7128, -74.0060)` and shifts them by `0.0005 * i` for any location entity. `spatial.py:30` hardcodes `resolved_coordinates=None`. |
| **Chronological Timeline** | `README.md:48, 70` | **FAKE** | `server.py:5007-5014` generates fake sequential timestamps `datetime.now() - timedelta(minutes=30 - i)` spaced by 1 minute, ignoring extracted temporal text. |
| **Cross-Statement Coreference** | `project_summary.md:22` | **FAKE** | `ml_core/extraction/ner.py:46` always returns `attributes={}`. `coref.py:99-103` requires shared attributes to link entities across statements, so cross-statement clustering never triggers. |
| **Negation Contradiction Override** | `README.md:123` | **BROKEN** | `ml_core/detection/rules.py:33-41` checks only `claim1.negated != claim2.negated`. Any negated claim paired with any non-negated claim (e.g. wearing a jacket vs not seeing a gun) is flagged as a 1.0 confidence contradiction without checking subject or action. |
| **Spatio-Temporal Extraction** | `README.md:120-122` | **BROKEN WIRING** | `ml_core/orchestrator.py:94-95` calls `extract_temporal_references` and `extract_spatial_references`, but variables `temporals` and `spatials` are never stored, aggregated, or returned in the output graph. |
| **Confidence Calibration (Isotonic Regression)** | `project_summary.md:25`, `IncidentWorkspace.tsx:313` | **FAKE** | `ml_core/detection/calibration.py:16` sets `self.is_fitted = False`. `calibrator.fit()` is never called anywhere in the codebase. `calibrate()` returns `raw_score` unmodified. `IncidentWorkspace.tsx:313` also claims `RoBERTa-large-MNLI`, which does not exist in the repo. |
| **Quantitative Pipeline Evaluation** | `README.md:402`, `capstone_report.tex:1022` | **FAKE** | `ml_core/tests/eval_pipeline.py:25-35` hardcodes constant metrics (`0.85, 0.88, 0.86`) and writes `eval_report.md`. It evaluates no model and no dataset. |
| **Testimony Ingestion Drawer** | `README.md:69`, `IngestionDrawer.tsx` | **FAKE** | `IngestionDrawer.tsx:28` runs a 4-second fake `setTimeout` UX animation. When submitted, `IncidentWorkspace.tsx:48-50` (`handleExtract`) only closes the drawer and discards the input without calling any API. |
| **Evidentiary Dossier PDF/CSV/Neo4j Export** | `IncidentWorkspace.tsx:345-360` | **FAKE** | `IncidentWorkspace.tsx:353` button click handler triggers `alert('... export is deferred to a future architecture phase.')`. `IncidentWorkspace.tsx:409` hardcodes `SHA256:{id}a3f7b2c9d1e4f83b1e7ff9d1c5e3...e692fabc`. |
| **Global Command Bar (Ctrl+K)** | `frontend/src/components/CommandBar.tsx` | **FAKE** | `CommandBar.tsx:26-30` searches only a hardcoded 3-element list (`Witness A`, `Red Sedan`, `Main St Collision`). |
| **Human-in-the-loop Feedback** | `README.md:417`, `project_summary.md:79` | **MISSING** | `ml_core/feedback.py:8-27` exists as an orphaned function. No backend route (`/api/feedback`) or UI integration exists. |
| **Persistent Storage** | `project_summary.md:61-65` | **FAKE** | `server.py:27-4892` stores all cases in a global in-memory dictionary taking up ~4,800 lines of code; all new cases disappear on restart. |
| **Configured Local LLM URL** | `README.md:303` | **BROKEN WIRING** | `README.md:303` documents `LOCAL_LLM_URL`, but `ml_core/llm_client.py:14` checks `LM_STUDIO_URL` and defaults to private IP `172.19.121.89:1234` instead of `127.0.0.1:1234`. |

---

## Issues by Severity

### Critical
1. **Frontend Production Build Failure (`frontend/src/components/RelationshipGraph.tsx:17, 49` & `frontend/src/pages/IncidentWorkspace.tsx:48, 225`):** Running `npm run build` fails with 5 TypeScript compilation errors (`TS7034`, `TS7005`, `TS6133`). CI/CD will fail and the app cannot be deployed to production.
2. **Silent Statement Replacement on Fallback (`server.py:4938-4954`):** If `analyze_incident()` throws any error (e.g., LM Studio is booting or slow), `server.py` silently throws away the user's actual submitted testimony, replaces `req.statements` with the 5 Tanishq robbery statements padded with 500 spaces (`+ " "*500`), and returns cached JSON.
3. **Unchecked Negation Contradiction Logic (`ml_core/detection/rules.py:33-41`):** `evaluate_negation_override` checks only `if claim1.negated != claim2.negated`. It never compares action or subject. If Witness A says "The robber wore a jacket" (`negated=False`) and Witness B says "I did not see a gun" (`negated=True`), the system declares a 1.0 confidence contradiction claiming one witness negated the other's claim.

### High
4. **Hardcoded Spatial Coordinates & Sequential Timestamps (`server.py:5007-5030`):** Map markers always use New York City coordinates `40.7128, -74.0060` with incremental offsets of `0.0005`, even for Indian scenarios. Timeline entries ignore extracted time and assign synthetic 1-minute steps (`datetime.now() - timedelta(minutes=30 - i)`).
5. **Fabricated Evaluation Metrics (`ml_core/tests/eval_pipeline.py:25-35`, `ml_core/eval_report.md:1-21`, `capstone_report.tex:1022-1029`):** `eval_pipeline.py` contains hardcoded numbers (`0.85`, `0.88`, `0.86`) and writes a fake report. These numbers were directly transcribed into the formal LaTeX report as experimental results.
6. **Broken Cross-Statement Coreference (`ml_core/extraction/ner.py:46`, `ml_core/extraction/coref.py:99-103`):** `ner.py` extracts entities with `attributes={}`. `coref.py` matches entities across statements only if they share attributes. Because attributes are never populated, cross-statement coreference is permanently a no-op.
7. **Discarded Spatio-Temporal Extractions (`ml_core/orchestrator.py:94-102`):** `temporals` and `spatials` are extracted via spaCy, but are kept in local variables and never added to the output graph or returned to the caller.

### Medium
8. **Fake Ingestion Drawer UX (`frontend/src/components/IngestionDrawer.tsx:28`, `frontend/src/pages/IncidentWorkspace.tsx:48-50`):** The drawer runs a fake 4-second `setTimeout` progress bar, then closes the drawer while discarding the user's entered witness name, date, location, and text.
9. **Fake Evidentiary Dossier & Custody Hash (`frontend/src/pages/IncidentWorkspace.tsx:353, 409`):** The export buttons only display browser alert boxes stating features are deferred. The custody SHA256 string contains literal hardcoded ellipsis (`...e692fabc`).
10. **Hardcoded Global Command Bar (`frontend/src/components/CommandBar.tsx:26-30`):** Searching via Ctrl+K searches only 3 static mock items.
11. **Environment Variable Inconsistency (`README.md:303`, `ml_core/llm_client.py:14`):** Documentation specifies `LOCAL_LLM_URL`, but code reads `LM_STUDIO_URL`, falling back to `http://172.19.121.89:1234`.
12. **Monolithic In-Memory Mock Database (`server.py:27-4892`):** `server.py` contains ~4,800 lines of hardcoded mock JSON dictionaries.
13. **Weak Test Suite Coverage (`ml_core/tests/`):** The 12 pytest tests all pass, but `test_coref.py:22` only asserts `len(resolved) == 4` without verifying resolution, and `test_cross_statement_coref` uses manually injected attributes not produced by the extractor. Zero tests exist for `align_claims`, `run_detection_pipeline`, or `server.py`.

### Low
14. **Compiled Bytecode Tracked in Git:** `.pyc` files in `ml_core/__pycache__/` and subdirectories are tracked in git instead of ignored.
15. **Hardcoded User Path in Test Script (`test_mapping.py:4`):** Contains hardcoded absolute Windows path `C:/Users/manik/Capstone_P1/theft_case_output.json`.
16. **Swallowed Exceptions (`ml_core/extraction/coref.py:44`, `ml_core/orchestrator.py:66`):** Bare `except Exception: pass` blocks hide potential failures.

---

## Placeholders and Hardcoded Values
- `server.py:27-4892` - 4,865 lines of in-memory canned JSON incidents and statements.
- `server.py:4949-4953` - Hardcoded Tanishq statements padded with 500 space characters (`+ " "*500`) to force span alignment on fallback.
- `server.py:5008` - `t = datetime.datetime.now() - datetime.timedelta(minutes=30 - i)` generates fake 1-minute sequential timestamps.
- `server.py:5019` - `base_lat, base_lng = 40.7128, -74.0060` uses New York City coordinates for all locations.
- `ml_core/llm_client.py:14` - `http://172.19.121.89:1234` hardcoded fallback LAN IP.
- `ml_core/extraction/spatial.py:30` - `resolved_coordinates=None` hardcoded stub.
- `ml_core/extraction/events.py:102, 107-108` - Prompt instructs LLM to output literal `"source_span": [0, 0]`.
- `ml_core/tests/eval_pipeline.py:26-32` - Synthetic precision/recall/F1 (`0.85`, `0.88`, `0.86`, `0.75`, `0.79`).
- `frontend/src/components/CommandBar.tsx:26-30` - Hardcoded 3-element array (`Witness A`, `Red Sedan`, `Main St Collision`).
- `frontend/src/pages/IncidentWorkspace.tsx:311` - Hardcoded bar width `style={{ width: '95%' }}`.
- `frontend/src/pages/IncidentWorkspace.tsx:313` - Hardcoded string `p=0.95 · RoBERTa-large-MNLI + isotonic calibration`.
- `frontend/src/pages/IncidentWorkspace.tsx:409-410` - Hardcoded literal hash `SHA256:{id}a3f7b2c9d1e4f83b1e7ff9d1c5e3...e692fabc`.
- `test_mapping.py:4` - Hardcoded path `C:/Users/manik/Capstone_P1/theft_case_output.json`.

---

## Incomplete and Dead Files
- `ml_core/feedback.py` - Orphaned module (`record_feedback`); never imported or called by any API route or UI component.
- `ml_core/detection/calibration.py` - Stub calibrator; `fit()` is never invoked; `is_fitted` remains permanently `False`.
- `generate_seed.py` / `inject_seed.py` - Ad-hoc scratch scripts sitting at repo root.
- `test_mapping.py` / `test_single_case.py` / `test_all.py` / `test_fallback.py` - Unstructured root-level test scripts with hardcoded URLs and paths.

---

## Verified by Running

### 1. Pytest Test Suite (`ml_core/tests/`)
- Command: `python -m pytest ml_core/tests/ -v`
- Result: **12 passed in 32.61s**.
- Observation: Tests pass because they rely heavily on mocks (`mock_llm`) or test trivial conditions (`assert len(resolved) == 4`).

### 2. Frontend Build (`frontend/`)
- Command: `npm run build` (`tsc -b && vite build`)
- Result: **FAILED (Exit Code 1)**
- Output:
  ```
  src/components/RelationshipGraph.tsx(17,11): error TS7034: Variable 'links' implicitly has type 'any[]' in some locations where its type cannot be determined.
  src/components/RelationshipGraph.tsx(49,14): error TS7005: Variable 'links' implicitly has an 'any[]' type.
  src/pages/IncidentWorkspace.tsx(48,26): error TS6133: 'meta' is declared but its value is never read.
  src/pages/IncidentWorkspace.tsx(48,37): error TS6133: 'text' is declared but its value is never read.
  src/pages/IncidentWorkspace.tsx(225,56): error TS6133: 'idx' is declared but its value is never read.
  ```

### 3. Backend Endpoints (`server.py`)
- `GET /` returns `{"status": "ok", "message": "Silent Witness Backend is running"}` (**200 OK**).
- `POST /api/incidents` successfully executes end-to-end ML pipeline with LM Studio on `http://172.25.171.202:1234` and returns structured contradiction JSON (**200 OK**).

---

## What Actually Works
1. **End-to-End Local LLM Ingestion & Inference:** The pipeline connects cleanly to LM Studio (via OpenAI API protocol) and successfully extracts event tuples and contradiction rationales.
2. **Semantic Vector Clustering:** Claims are embedded with `all-MiniLM-L6-v2` and clustered with `AgglomerativeClustering`.
3. **Credibility Language Guardrails:** The denylist filter (`pipeline.py:9-18`) effectively replaces judgmental language with non-adjudicative phrasing.
4. **Synthetic Test Data:** All 20 scenarios (400 eyewitness transcripts) and 100 benchmark incident JSON files exist and have substantial, realistic content.
5. **Interactive UI (in Dev Mode):** When run via `npm run dev`, Vite runs and renders the multi-tab layout, Vis-Timeline, Leaflet map, and side-by-side statement comparison.

---

## Prioritized Fix Plan

1. **Fix TypeScript build errors (`RelationshipGraph.tsx`, `IncidentWorkspace.tsx`)** to allow `npm run build` to pass.
2. **Fix negation contradiction comparator (`ml_core/detection/rules.py:33`)** so that `evaluate_negation_override` checks for matching subjects/actions before declaring a contradiction.
3. **Wire extracted spatio-temporal references into the output graph (`ml_core/orchestrator.py:94-102`)** so spatial and temporal data are actually returned to the server.
4. **Remove fake NYC coordinates and synthetic 1-minute timestamps (`server.py:5007-5030`)**; map real extracted timestamps and locations to the frontend schema.
5. **Populate entity attributes in `ner.py`** so that cross-statement coreference in `coref.py` can function as claimed.
6. **Connect `IngestionDrawer.tsx` to `createIncident()` API** instead of dropping user input after the fake animation.
7. **Fix environment variable lookup in `ml_core/llm_client.py:14`** to check `LOCAL_LLM_URL` as documented, defaulting to `127.0.0.1:1234`.
8. **Replace fabricated evaluation code (`eval_pipeline.py`)** with a real evaluation script that runs benchmark incidents from `ml_core/synthetic/generated/` and computes true precision, recall, and F1.
9. **Remove `theft_case_output.json` statement overwrite hack (`server.py:4948-4954`)**; return an explicit error or honest notification if the ML pipeline fails.
10. **Git hygiene cleanup:** Untrack `.pyc` files from git history and add them to `.gitignore`.
