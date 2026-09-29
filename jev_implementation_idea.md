# Jev by TypeSafe AI — Implementation Ideas for Silent Witness

> **Status:** Research & Ideation  
> **Date:** September 2026  
> **Author:** Harshit Mishra  
> **Purpose:** Explore how TypeSafe AI's Jev (System One model) can enhance the Silent Witness contradiction detection pipeline.

---

## 1. What Is Jev / System One?

**Jev** is TypeSafe AI's flagship **System One model** — a class of AI model fundamentally different from LLMs like ChatGPT or SmolLM-3B. Instead of *generating text*, it returns **typed, probabilistic, structured judgments** that code can consume directly.

| | **SmolLM-3B (current)** | **Jev / System One** |
| :--- | :--- | :--- |
| **What it does** | Generates free text → you parse JSON from it | Returns clean `{ choice: "X", probability: 0.95, confidence: 0.91 }` |
| **Speed** | ~45 seconds for 5 witnesses | ~100ms per decision |
| **Output** | Unpredictable, needs sanitizers | Fully typed, always valid |
| **Hallucination** | Possible | Constrained to the options you define |
| **Cost model** | Free (local) | Token-based (cloud API) |
| **Control** | LLM controls phrasing | Your code controls logic |

### The Three Primitives

Jev exposes three question types you design upfront:

- **`Noul`** — returns a probability 0–1 for a yes/no question  
  _e.g., "Do these two claims contradict on clothing?" → `0.94`_
- **`Choice`** — picks one option from a defined set  
  _e.g., "What type of contradiction is this?" → `"attire"`_
- **`Score`** — rates along ordered descriptive levels  
  _e.g., "How severe is this contradiction?" → `1.7` on a 0–2 scale_

**Key advantage:** Ask 10 parallel questions in one API call, all evaluated simultaneously in ~100ms.

---

## 2. Where Does Jev Fit in the Architecture?

The Silent Witness pipeline has 5 stages. Jev is a **surgical enhancement** to exactly 3 of them:

```
[Raw Statements]
     │
     ▼
Stage 1: spaCy NER & Negation          ← KEEP AS-IS (fast, free, deterministic)
     │
     ▼
Stage 2: SmolLM Event Extraction       ← KEEP AS-IS (local privacy requirement)
     │
     ▼
Stage 3: Semantic Vector Clustering    ← KEEP AS-IS (MiniLM works well)
     │
     ▼
Stage 3.5: Jev Entity Alignment    ────┤ JEV ADDS: cross-witness entity matching
     │                                 │ ("red car" = "the sedan"?)
     ▼                                 │
Stage 4: Contradiction Detection  ─────┤ JEV REPLACES: local_nli_predict()
     │                                 │ JEV REPLACES: generate_nli_rationale()
     │                                 │ JEV ADDS: claim type classification
     │                                 │ JEV ADDS: confidence-gated escalation
     ▼                                 │
Stage 5: Structured JSON Output   ─────┘ JEV ADDS: severity scores for UI badges
```

---

## 3. Full Architecture Diagram with Jev

```
[5 Witness Statements]
         │
         ▼
┌─────────────────────────────────────────────┐
│  Stage 1: spaCy NER + Negation Parser       │  ← Unchanged (local, fast)
│  → Entities, Times, Locations, Denial flags │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  Stage 2: SmolLM-3B Event Extraction        │  ← Unchanged (100% local, privacy safe)
│  (LM Studio) → (Subject, Action, Object)    │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  Stage 3: MiniLM Semantic Vector Clustering │  ← Unchanged (groups by topic)
│  → [clothing claims] [escape claims] ...    │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐   ◄── JEV: Entity Alignment
│  Stage 3.5: Jev Cross-Witness Entity Check  │
│  Noul: "Do 'the red car' and 'the sedan'    │
│  refer to the same vehicle?" → 0.91         │
│  → merge / separate / flag for human review │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐   ◄── JEV: Core Contradiction Role
│  Stage 4: Jev Contradiction Detection       │
│  Per aligned pair, ONE call, 5 questions:   │
│  • is_contradiction:    Noul  → 0.94        │
│  • contradiction_type:  Choice → "attire"   │
│  • severity:            Score → 1.8 / 2.0   │
│  • is_denial_vs_claim:  Noul  → 0.89        │
│  • are_paraphrases:     Noul  → 0.06        │
│                                             │
│  Confidence Gate:                           │
│  conf ≥ 0.85 → auto_flag (show in UI)      │
│  conf 0.5–0.85 → flag_for_review           │
│  conf < 0.5 → escalate to SmolLM           │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  Stage 5: FastAPI JSON Output + React UI    │
│  • Contradiction Panel: filtered by type    │
│  • Severity color badges (Score → RGB)      │
│  • "Needs Review" flags from confidence gate│
│  • Human-in-the-loop feedback endpoint      │
└─────────────────────────────────────────────┘
```

---

## 4. Integration Point 1 — Contradiction Detection

**Current problem:** `local_nli_predict()` in [`ml_core/orchestrator.py`](ml_core/orchestrator.py) asks SmolLM-3B an open-ended question, parses raw JSON from text (fragile), and takes seconds per call.

**Jev replacement — 5 parallel atomic questions per claim pair, in one ~100ms call:**

```python
# ml_core/detection/jev_detector.py
from typesafe_sdk import TypeSafeClient, Noul, Score, Choice
import os

client = TypeSafeClient(api_key=os.environ["TYPESAFE_API_KEY"])

def jev_detect_contradiction(claim1_text: str, claim2_text: str) -> dict:
    """
    Replaces local_nli_predict() + generate_nli_rationale().
    Asks 5 atomic, parallel questions in a SINGLE API call (~100ms).
    """
    response = client.system_one(
        state={
            "claim_a": claim1_text,
            "claim_b": claim2_text,
        },
        questions={
            # Core: is there a factual contradiction?
            "is_contradiction": Noul(
                instructions="Do `claim_a` and `claim_b` describe the same observable fact "
                             "differently in a way that cannot both be true?"
            ),
            # Classification: what dimension is the clash on?
            "contradiction_type": Choice(
                instructions="Which factual dimension does the primary conflict between "
                             "`claim_a` and `claim_b` fall into?",
                criteria={
                    "attire":       "Clothing, appearance, or physical description of a person",
                    "weapon":       "Presence, type, or use of a weapon or tool",
                    "escape_route": "Direction, vehicle, or method of departure",
                    "headcount":    "Number of suspects, victims, or bystanders",
                    "timing":       "Time of day, sequence of events, or duration",
                    "location":     "Specific place, landmark, or spatial reference",
                    "no_conflict":  "No substantive conflict is present",
                }
            ),
            # Severity: how serious is the contradiction?
            "severity": Score(
                instructions="How directly and unambiguously do `claim_a` and `claim_b` "
                             "contradict each other?",
                criteria=[
                    "The claims describe clearly compatible facts; no contradiction.",
                    "There is a minor discrepancy that could be explained by vantage point.",
                    "There is a clear factual mismatch that cannot be reconciled."
                ]
            ),
            # Negation guard: one denies what the other asserts?
            "is_denial_vs_assertion": Noul(
                instructions="Does one of `claim_a` or `claim_b` explicitly deny an action "
                             "that the other explicitly asserts?"
            ),
            # Paraphrase guard: same thing said differently?
            "are_paraphrases": Noul(
                instructions="Do `claim_a` and `claim_b` express the same underlying fact "
                             "using different words?"
            ),
        }
    )
    answers = response.answers

    # All control flow stays in Python — code is in control, not the model
    is_contradiction = answers["is_contradiction"].noul > 0.7
    are_paraphrases  = answers["are_paraphrases"].noul > 0.75

    if are_paraphrases or not is_contradiction:
        return {"verdict": "corroboration", "confidence": answers["are_paraphrases"].noul}

    return {
        "verdict":            "contradiction",
        "confidence":         answers["is_contradiction"].noul,
        "contradiction_type": answers["contradiction_type"].choice,
        "severity":           answers["severity"].score,
        "is_denial":          answers["is_denial_vs_assertion"].noul > 0.8,
        "model_confidence":   answers["contradiction_type"].confidence,
    }
```

**Why this beats the current approach:**
- Current code calls SmolLM, gets raw text, needs 3 regex/JSON sanitizers to recover `true/false`. Jev returns clean typed objects.
- Current code asks one broad question. Jev asks 5 narrow atomic questions in parallel — each independently inspectable and composable.
- `contradiction_type` maps directly to the React UI's Analysis Panel filter tabs.
- `severity` score drives visual color coding in the frontend (green → yellow → red).

---

## 5. Integration Point 2 — Claim Alignment Verification

**Current problem:** MiniLM clusters claims by vector proximity. Sometimes claims that are semantically similar but *not about the same incident detail* get grouped together, causing false contradiction flags.

**Jev fix — verify alignment quality before comparing:**

```python
def jev_verify_alignment(claim_a: str, claim_b: str) -> bool:
    """
    Before running contradiction detection, confirm the two claims are
    actually about the same observable dimension of the incident.
    """
    response = client.system_one(
        state={"claim_a": claim_a, "claim_b": claim_b},
        questions={
            "same_subject_matter": Noul(
                instructions="Do `claim_a` and `claim_b` describe the same specific "
                             "observable dimension — e.g. both about a suspect's clothing, "
                             "or both about the escape vehicle?"
            ),
        }
    )
    # Only run full NLI comparison if Jev confirms they're about the same thing
    return response.answers["same_subject_matter"].noul > 0.65
```

This prevents flagging `"He wore a leather jacket"` vs `"She screamed for help"` as a contradiction just because MiniLM happened to cluster them nearby.

---

## 6. Integration Point 3 — Confidence-Gated Human Escalation

This is the highest-value architectural addition. Jev's **confidence** score (not the probability, but how certain Jev is about its own answer) tells you whether to act automatically or escalate to a human or reasoning model.

```python
def jev_route_contradiction(claim_a: str, claim_b: str) -> dict:
    result = jev_detect_contradiction(claim_a, claim_b)
    model_confidence = result.get("model_confidence", 0.0)

    if model_confidence >= 0.85:
        # High confidence: surface automatically in the UI
        return {**result, "action": "auto_flag", "requires_review": False}
    elif model_confidence >= 0.5:
        # Medium confidence: flag but mark for investigator review
        return {**result, "action": "flag_for_review", "requires_review": True}
    else:
        # Low confidence: escalate to local SmolLM for deep analysis
        rationale = call_local_llm(
            f"Analyze carefully: do these contradict?\nA: {claim_a}\nB: {claim_b}"
        )
        return {**result, "action": "escalated", "rationale": rationale, "requires_review": True}
```

**In the React frontend, this maps directly to:**

| Action | UI Badge | Investigator Action |
| :--- | :--- | :--- |
| `auto_flag` | 🔴 Red — "Contradiction Detected" | Shown immediately |
| `flag_for_review` | 🟡 Amber — "Needs Review" | Investigator confirms/dismisses |
| `escalated` | ⬜ Grey — "Under Analysis" | SmolLM rationale attached |

---

## 7. Integration Point 4 — Entity Alignment (Cross-Witness Coreference)

Current coreference resolution uses simple heuristics. Jev's **Entity Alignment** pattern (from the [entity_alignment cookbook](https://docs.typesafe.ai/cookbooks/entity_alignment.md)) is a perfect fit for matching `"the red car"` in Witness 1 with `"the sedan"` in Witness 2:

```python
def jev_align_entities(
    entity_a: str, entity_b: str,
    context_a: str, context_b: str
) -> str:
    """
    Decides if two entity mentions across witnesses refer to the same thing.
    Returns: "same_entity", "curator_queue", or "different_entity"
    """
    response = client.system_one(
        state={
            "mention_a": {"text": entity_a, "witness_context": context_a},
            "mention_b": {"text": entity_b, "witness_context": context_b},
        },
        questions={
            "entity_match": Score(
                instructions="How likely are `mention_a` and `mention_b` to refer to "
                             "the same real-world entity?",
                criteria=[
                    "They almost certainly refer to different entities.",
                    "Possibly the same entity — context is ambiguous, needs human review.",
                    "Almost certainly the same entity described differently."
                ]
            ),
            "same_vehicle_type": Noul(
                instructions="If both mentions refer to vehicles, do they describe the "
                             "same vehicle class or type?"
            ),
            "same_person": Noul(
                instructions="If both mentions refer to people, do the descriptions "
                             "indicate the same individual?"
            ),
        }
    )
    score = response.answers["entity_match"].score
    if score >= 1.5: return "same_entity"
    if score >= 0.5: return "curator_queue"
    return "different_entity"
```

---

## 8. Impact Summary

| Problem Today | With Jev |
| :--- | :--- |
| `local_nli_predict()` parses brittle JSON from LLM text output | Clean typed `{ noul: 0.94, confidence: 0.91 }` — zero parsing needed |
| One broad "do these contradict?" question | 5 parallel atomic questions in ~100ms: type, severity, denial, paraphrase guard |
| No confidence calibration — all contradictions weighted equally | Calibrated confidence score routes to auto-flag / review / SmolLM escalation |
| Contradiction panel shows everything with the same weight | `contradiction_type` field directly drives UI filter tabs |
| `severity` is not computed | Jev `Score` value drives color badges in the React frontend |
| Entity alignment is keyword/heuristic matching | Jev `Score` + `Noul` aligns "the red car" with "the sedan" semantically |
| No human-in-the-loop pathway | Confidence gate triggers "Needs Review" badges in the frontend |

---

## 9. Important Privacy Constraint & Hybrid Design

Jev is a **cloud API** — it requires a `TYPESAFE_API_KEY` and sends data to TypeSafe's servers. This creates a **privacy tension** with Silent Witness's 100% local design principle for sensitive police testimonies.

### Recommended Hybrid Architecture

```
Raw Testimony Text         → SmolLM-3B (Stage 2, LOCAL)
                                     ↓
Extracted Claim Tuples     → Jev (Stage 4, CLOUD)
"robber wore leather jacket" vs "suspect wore red hoodie"
```

- **Stage 2 (raw text extraction):** SmolLM-3B runs 100% locally — PII-containing full testimonies never leave the machine.
- **Stage 4 (claim comparison):** Only clean, extracted, de-contextualized claim tuples like `"wore leather jacket"` and `"wore red hoodie"` are sent to Jev. These contain minimal PII and maximum forensic signal.

This keeps the legal privacy guarantee intact while leveraging Jev's speed and structured precision for the comparison task.

---

## 10. Getting Started with Jev

```bash
pip install typesafe-sdk
export TYPESAFE_API_KEY="your-key-here"
```

```python
from typesafe_sdk import TypeSafeClient, Noul
client = TypeSafeClient()

response = client.system_one(
    state={
        "claim_a": "The robber wore a dark leather jacket.",
        "claim_b": "The suspect had on a bright red hoodie.",
    },
    questions={
        "is_contradiction": Noul(
            instructions="Do `claim_a` and `claim_b` describe the same person's "
                         "attire in ways that cannot both be true?"
        )
    }
)
print(response.answers["is_contradiction"].noul)  # e.g. 0.97
```

### Docs & References
- [TypeSafe AI Documentation Index](https://docs.typesafe.ai/llms.txt)
- [System One Concept](https://docs.typesafe.ai/concepts/system-one.md)
- [How to Build with TypeSafe](https://docs.typesafe.ai/concepts/how-to-build-with-system-one.md)
- [Entity Alignment Cookbook](https://docs.typesafe.ai/cookbooks/entity_alignment.md) ← Most relevant to Silent Witness
- [Citation Check Cookbook](https://docs.typesafe.ai/cookbooks/citation_check.md) ← Useful for claim verification
- [Confidence-Gated Routing Pattern](https://docs.typesafe.ai/patterns/confidence-routing.md)
- [Parallel Questions Cookbook](https://docs.typesafe.ai/cookbooks/parallel_questions.md) ← Ask all 5 questions in one call
- [Python SDK](https://docs.typesafe.ai/sdk/python.md)
