import uuid
import logging
from typing import List, Dict, Any

from ml_core.schema.models import Statement, Entity, EventTuple, Claim, DetectionResult
from ml_core.extraction.ner import extract_entities
from ml_core.extraction.temporal import extract_temporal_references
from ml_core.extraction.spatial import extract_spatial_references
from ml_core.extraction.events import extract_events_llm
from ml_core.extraction.negation import apply_negation_scoping
from ml_core.extraction.coref import resolve_single_document_coref, resolve_cross_statement_coref
from ml_core.alignment.cluster import align_claims
from ml_core.detection.pipeline import run_detection_pipeline
from ml_core.llm_client import call_local_llm

logger = logging.getLogger(__name__)

# Dummy NLI prediction function (if roberta is too heavy to load instantly, we simulate it for the demo)
def dummy_nli_predict(text1: str, text2: str) -> float:
    # If the texts are identical, no contradiction
    if text1 == text2: return 0.0
    # For demo purposes, we randomly assign a score or rely purely on rules
    return 0.2

# Dummy rationale generation
def local_rationale_gen(prompt: str) -> str:
    # In a full system, you could use call_local_llm here as well.
    # We will use a fast fallback template for the demo.
    return "The witnesses provided conflicting details regarding this event."

def analyze_incident(raw_statements: List[str]) -> Dict[str, Any]:
    """
    End-to-End Orchestrator:
    Takes a list of raw string testimonies and runs the entire ML pipeline locally.
    """
    all_statements = []
    all_entities = []
    all_events = []
    all_occurrences = []
    
    # 1. Base Extraction Loop
    for idx, text in enumerate(raw_statements):
        stmt = Statement(
            id=f"stmt_{idx}",
            witness_id=f"wit_{idx}",
            text=text,
            incident_id="demo_incident"
        )
        all_statements.append(stmt)
        
        # Local ML deterministic passes
        entities = extract_entities(stmt)
        temporals = extract_temporal_references(stmt)
        spatials = extract_spatial_references(stmt)
        
        # Coref (intra-doc)
        entities = resolve_single_document_coref(stmt, entities)
        
        # Merge all into the pool
        all_entities.extend(entities)
        
        # LLM Event Pass (SmolLM via LM Studio)
        try:
            events, occurrences = extract_events_llm(stmt, call_local_llm, sample_count=1) # Reduced to 1 for speed
        except Exception as e:
            logger.error(f"Event extraction failed for {stmt.id}: {e}")
            events, occurrences = [], []
            
        events = apply_negation_scoping(stmt, events)
        
        all_events.extend(events)
        all_occurrences.extend(occurrences)
        
    # 2. Cross-Document Alignment
    all_entities = resolve_cross_statement_coref(all_statements, all_entities)
    
    # Create claims (binding events + their local entities)
    claims = []
    for ev in all_events:
        # Find entities in the same statement
        local_ents = [e for e in all_entities if e.source_statement_id == ev.source_statement_id]
        claims.append(Claim(id=str(uuid.uuid4()), event=ev, entities=local_ents))
        
    # Cluster claims about the same incident
    claim_clusters = align_claims(claims)
    
    # 3. Contradiction Detection
    # Run the detection pipeline over the events
    detections = run_detection_pipeline(
        occurrences=all_occurrences,
        events=all_events,
        nli_model_predict=dummy_nli_predict,
        llm_rationale_gen=local_rationale_gen
    )
    
    # 4. Format Output Graph
    return {
        "status": "success",
        "metrics": {
            "total_statements": len(raw_statements),
            "total_entities": len(all_entities),
            "total_events": len(all_events),
            "total_claims": len(claims),
            "total_contradictions": len(detections)
        },
        "entities": [e.__dict__ for e in all_entities],
        "events": [ev.__dict__ for ev in all_events],
        "contradictions": [d.__dict__ for d in detections]
    }
