from typing import List, Optional
from ml_core.schema.models import EventOccurrence, EventTuple, DetectionResult

def check_existence_contradictions(occurrences: List[EventOccurrence], events: List[EventTuple]) -> List[DetectionResult]:
    """
    Checks for existence contradictions (Step 4).
    Compares explicit EventOccurrence denials against EventTuple assertions.
    """
    results = []
    
    for occ in occurrences:
        if occ.occurred is False:
            # Find any EventTuple from a DIFFERENT witness with the same action
            for ev in events:
                if occ.source_statement_id != ev.source_statement_id and occ.event_type == ev.action:
                    # Direct existence contradiction
                    results.append(DetectionResult(
                        claim_ids=[],  # To be populated by pipeline
                        type="existence",
                        verdict="contradiction",
                        confidence=1.0,
                        rationale=f"One witness stated that the action '{occ.event_type}' did not happen, while another described it happening.",
                        source_span=[(occ.source_statement_id, occ.source_span), (ev.source_statement_id, ev.source_span)]
                    ))

    return results

def evaluate_negation_override(claim1: EventTuple, claim2: EventTuple) -> Optional[DetectionResult]:
    """
    Evaluates a pair of aligned claims for negation-based hard overrides (Step 3).
    Returns a contradiction if exactly one claim is negated AND both claims
    refer to the same action or targeted object/entity.
    """
    if claim1.negated != claim2.negated:
        act1 = (claim1.action or "").lower().strip()
        act2 = (claim2.action or "").lower().strip()
        
        # Check action semantic compatibility
        actions_match = False
        if act1 and act2:
            if act1 == act2 or act1 in act2 or act2 in act1:
                actions_match = True
            elif {act1, act2} in [
                {"see", "saw"}, {"flee", "fled"}, {"run", "ran"}, 
                {"shoot", "shot"}, {"enter", "entered"}, {"drive", "drove"},
                {"carry", "carried"}, {"wear", "wore"}, {"hold", "held"}
            ]:
                actions_match = True
                
        obj1 = (claim1.object or "").lower().strip()
        obj2 = (claim2.object or "").lower().strip()
        objects_overlap = bool(obj1 and obj2 and (obj1 in obj2 or obj2 in obj1))
        
        if actions_match or (objects_overlap and (act1 in ["see", "saw", "have", "had", "notice", "spot"] or act2 in ["see", "saw", "have", "had", "notice", "spot"])):
            return DetectionResult(
                claim_ids=[], # To be populated by pipeline
                type="existence",
                verdict="contradiction",
                confidence=1.0,
                rationale="One witness explicitly negated this claim, while the other asserted it.",
                source_span=[(claim1.source_statement_id, claim1.source_span), (claim2.source_statement_id, claim2.source_span)]
            )
        
    return None
