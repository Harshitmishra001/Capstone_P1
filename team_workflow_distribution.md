# Silent Witness — Complete Workflow & Team Distribution

## 👥 Team Composition (6 Members)

| Role | Member | Name | Primary Focus |
| :--- | :--- | :--- | :--- |
| **Frontend 1** | **FE1** | **Manik Pandey** | Core UI, React architecture, routing, statement ingestion, state management, and API client integration. |
| **Frontend 2** | **FE2** | **Tushar Saxena** | Visualization UI, Vis-Timeline integration, Leaflet maps, spatio-temporal interactivity, and cross-component highlighting. |
| **Backend 1** | **BE1** | **Harshit Mishra** | ML/NLP Engineer. Core Python pipeline, extractors (NER, events), alignment, contradiction detection, and NLI models. |
| **Backend 2** | **BE2** | **Mahi Saxena** | Data & Infrastructure Engineer. Neo4j graph schemas, Celery + Redis task queues, DB queries, and containerization. |
| **API** | **API1** | **Harsh** | FastAPI routing, JWT authentication, controller logic, external integrations (e.g., Nominatim), and report generation. |
| **Documentation & QA** | **DOC1** | **Partishta** | Technical Writer & QA Engineer. CI/CD pipelines, automated testing (pytest/Playwright), architecture diagrams, logging hooks, and capstone defense materials. |

---

## 🚀 Workflow Phases & Task Breakdown

### Phase 1: ML Core (Standalone Pipeline)
*Goal: Prove the ML extraction and detection works perfectly in isolation before building the app.*

- **Harshit (BE1):** Build synthetic dataset generator. Implement NER, Temporal/Spatial extractors, Claim Alignment, and Detection Engine (Rules + NLI).
- **Mahi (BE2):** Set up local environment, assist with Python project structure, and design initial Neo4j graph data models conceptually.
- **Harsh (API1):** Design the internal `pipeline.run()` interface and draft API contracts (Swagger/OpenAPI specifications) for the frontend team.
- **Manik (FE1) & Tushar (FE2):** Evaluate UI libraries (vis-timeline, Leaflet), set up React + Vite boilerplate, and build static HTML/CSS mockups (like `demo.html`).
- **Partishta (DOC1):** Write and implement the `pytest` suite for the ML core. Document the dataset generation strategy and define ML schemas.

### Phase 2: Backend & API Integration
*Goal: Wrap the ML core in a robust, async microservice architecture.*

- **Harsh (API1):** Build FastAPI service, implement JWT Auth, create CRUD endpoints for incidents and statements.
- **Mahi (BE2):** Deploy Neo4j and Redis. Implement Celery workers to run the ML pipeline asynchronously. Write DB queries (Cypher).
- **Harshit (BE1):** Refine ML pipeline based on integration testing, package ML core as a standalone callable module.
- **Manik (FE1):** Build API client layer in React (`api/client.ts`), implement JWT auth flow, and build Ingestion forms.
- **Tushar (FE2):** Create data adaptors to transform API JSON responses into Vis-Timeline and Leaflet compatible formats.
- **Partishta (DOC1):** Set up CI/CD pipelines (GitHub Actions) for automatic testing. Write automated API integration tests (`pytest`) and document endpoints (Postman/Swagger).

### Phase 3: Frontend Functional Integration (MVP)
*Goal: Connect the frontend to the real backend API for end-to-end functionality.*

- **Manik (FE1):** Implement Contradiction/Agreement panel, connect statement submission to async polling (`GET /jobs/{id}`).
- **Tushar (FE2):** Render dynamic Timeline and Map views using real API data. Implement source-span click-to-highlight functionality.
- **Harsh (API1):** Build PDF/CSV Export endpoints, support frontend integration debugging.
- **Mahi (BE2):** Optimize Neo4j queries for fast timeline and map data retrieval.
- **Harshit (BE1):** Tune confidence thresholds and calibrate NLI based on full-system tests.
- **Partishta (DOC1):** Implement End-to-End (E2E) automated tests (Playwright/Cypress) for the MVP UI. Conduct initial Usability Walkthroughs with non-team testers.

### Phase 4: Visualization Polish & Graph Hardening
*Goal: Perfect the unified spatio-temporal UI (the project's main USP).*

- **Manik (FE1) & Tushar (FE2):** Unify visual language (witness color coding). Implement timeline ↔ map linkage (time-scrubber, synchronized highlighting). Handle dense marker clustering.
- **Harsh (API1):** Implement geocoding caching (Nominatim) to prevent rate-limiting, refine payload sizes for dense graphs.
- **Harshit (BE1) & Mahi (BE2):** Implement incremental statement addition (only processing new claims). Fix any edge-cases in claim alignment.
- **Partishta (DOC1):** Implement telemetry/logging hooks for performance monitoring. Finalize architecture diagrams and write user guides for the visual timeline/map.

### Phase 5: Hardening, Evaluation & Capstone Defense
*Goal: Finalize metrics, secure the application, and prepare for grading.*

- **Harshit (BE1):** Run final synthetic evaluation script, generate final `eval_report.md` (target ≥ 0.80 F1).
- **Mahi (BE2):** Containerize the entire stack (Docker Compose) for reproducible demo deployment.
- **Harsh (API1):** Security audit (JWT enforcement, endpoint security), prepare final API documentation for defense.
- **Manik (FE1) & Tushar (FE2):** Cross-browser testing, responsive UI fixes, accessibility pass.
- **Partishta (DOC1):** Compile the final Capstone Report and slide deck. Manage containerized test runs and compile the final real-world validation data script.
