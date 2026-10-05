# Silent Witness API Documentation

This document provides a comprehensive, Swagger-style OpenAPI reference for the Silent Witness FastAPI backend.

**Base URL:** `http://127.0.0.1:8000`  
**Version:** `1.0.0`  
**Interactive Docs (Swagger UI):** `http://127.0.0.1:8000/docs`  
**Alternative Docs (ReDoc):** `http://127.0.0.1:8000/redoc`

---

## 📌 Endpoints

### 1. Health Check
`GET /`

Returns the health status of the backend server. Use this to verify that the FastAPI server and Uvicorn are running correctly.

**Parameters**
* No parameters required.

**Responses**
* **200 OK**
  * **Content-Type:** `application/json`
  * **Example:**
    ```json
    {
      "status": "ok",
      "message": "Silent Witness Backend is running"
    }
    ```

---

### 2. Analyze Incident Statements
`POST /analyze`

Orchestrates the entire 5-stage ML pipeline. It ingests raw eyewitness testimonies, extracts entities and events, groups them into semantic clusters, runs the contradiction detection engine (Rules + NLI), and outputs a structured evidentiary graph.

**Request Body**
* **Content-Type:** `application/json`
* **Schema:** [`IncidentRequest`](#incidentrequest)
* **Example:**
  ```json
  {
    "statements": [
      "Two masked robbers stormed in. The primary robber wore a dark leather jacket.",
      "Three guys ran out. The lead robber had a bright red hoodie and a silver gun."
    ]
  }
  ```

**Responses**
* **200 OK** — Successfully processed the incident.
  * **Content-Type:** `application/json`
  * **Schema:** [`AnalysisResponse`](#analysisresponse)
  * **Example:**
    ```json
    {
      "status": "success",
      "metrics": {
        "total_statements": 2,
        "total_entities": 4,
        "total_events": 6,
        "total_claims": 6,
        "total_contradictions": 1
      },
      "entities": [ ... ],
      "events": [ ... ],
      "contradictions": [
        {
          "claim_ids": ["claim_2", "claim_5"],
          "type": "semantic",
          "verdict": "contradiction",
          "confidence": 0.94,
          "rationale": "One account describes the suspect wearing a dark leather jacket, while another describes a bright red hoodie.",
          "source_span": [
            ["stmt_0", [154, 175]],
            ["stmt_1", [48, 65]]
          ]
        }
      ]
    }
    ```

* **400 Bad Request** — Invalid input data.
  * **Example:** `{"detail": "Must provide at least one statement."}`

* **422 Validation Error** — Pydantic schema validation failed.
  * **Example:** `{"detail": [{"loc": ["body", "statements"], "msg": "field required", "type": "value_error.missing"}]}`

* **500 Internal Server Error** — The ML pipeline encountered a fatal execution error (e.g., LM Studio is down).

---

## 🧩 Data Schemas / Models

### `IncidentRequest`
The payload for submitting testimonies.
| Field | Type | Required | Description |
|---|---|---|---|
| `statements` | `Array of strings` | Yes | A list of raw text eyewitness testimonies. Each string represents one witness's full account. |

---

### `AnalysisResponse`
The root response object returned by `/analyze`.
| Field | Type | Description |
|---|---|---|
| `status` | `string` | Execution status (e.g., `"success"`). |
| `metrics` | `object` | Execution metrics (statement, entity, event, and contradiction counts). |
| `entities` | `Array<Entity>` | List of all named entities extracted (Persons, Vehicles, Objects, Locations). |
| `events` | `Array<EventTuple>` | List of all atomic action events extracted. |
| `contradictions` | `Array<DetectionResult>` | List of all detected factual divergences and their source rationales. |

---

### `Entity`
Represents an extracted physical entity. Inherits from `ExtractedBase` for traceability.
| Field | Type | Description |
|---|---|---|
| `source_statement_id` | `string` | The ID of the statement (e.g., `"stmt_0"`). |
| `source_span` | `[int, int]` | `[start_char, end_char]` relative to the original statement string. |
| `text` | `string` | The exact extracted string. |
| `label` | `string` | The domain type: `PERSON`, `VEHICLE`, `OBJECT`, or `LOCATION`. |
| `attributes` | `object` | Key-value properties (e.g., color, make). |
| `entity_cluster_id` | `string` | UUID linking this entity to co-referent entities across testimonies. |

---

### `EventTuple`
Represents an atomic extracted action (Subject-Action-Object). Inherits from `ExtractedBase`.
| Field | Type | Description |
|---|---|---|
| `source_statement_id` | `string` | The ID of the statement. |
| `source_span` | `[int, int]` | Character offsets marking the source. |
| `text` | `string` | The snippet describing the event. |
| `subject` | `string` | Who or what performed the action. |
| `action` | `string` | The verb or core action. |
| `object` | `string` | The target of the action. |
| `confidence` | `float` | Pipeline confidence in the extraction (0.0 to 1.0). |
| `low_confidence`| `boolean`| True if the LLM self-consistency loop had < 50% agreement. |
| `negated` | `boolean` | True if the action was explicitly denied in the text (e.g., "did not shoot"). |

---

### `DetectionResult`
Represents a flagged contradiction or corroboration.
| Field | Type | Description |
|---|---|---|
| `claim_ids` | `Array<string>` | IDs of the conflicting claims. |
| `type` | `string` | Category of conflict: `attribute`, `spatial`, `temporal`, `existence`, or `semantic`. |
| `verdict` | `string` | Result verdict, usually `"contradiction"`. |
| `confidence` | `float` | Calibrated probability of a contradiction (0.0 to 1.0). |
| `rationale` | `string` | An LLM-generated, neutral factual explanation of the mismatch. Filtered by the non-adjudicative denylist. |
| `source_span` | `Array` | A list of `[statement_id, [start, end]]` arrays, mapping the exact character location of both conflicting statements for UI highlighting. |

---

## 🚀 Usage Example (cURL)

You can test the endpoint directly from your terminal while the FastAPI server is running:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/analyze' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "statements": [
    "I was at the counter. The thief was wearing a blue jacket and ran out the front door.",
    "I was outside. A man in a red coat came running out the front door carrying a bag."
  ]
}'
```
