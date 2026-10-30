from typing import List, Optional, Set
from ml_core.schema.models import EventOccurrence, EventTuple, DetectionResult

ACTION_SYNONYMS = [
    {"see", "saw", "seen", "notice", "noticed", "spot", "spotted", "observe", "observed", "witness", "witnessed"},
    {"flee", "fled", "fleeing", "escape", "escaped", "run", "ran", "running"},
    {"shoot", "shot", "shooting", "fire", "fired", "firing"},
    {"enter", "entered", "entering", "walk in", "walked in", "came in", "come in"},
    {"drive", "drove", "driving"},
    {"carry", "carried", "carrying", "hold", "held", "holding"},
    {"wear", "wore", "wearing"},
    {"have", "had", "having", "possess", "possessed"},
    {"steal", "stole", "stolen", "loot", "looted", "take", "took", "taken"},
]

def _actions_are_compatible(act1: str, act2: str) -> bool:
    if not act1 or not act2:
        return False
    a1, a2 = act1.lower().strip(), act2.lower().strip()
    if a1 == a2 or a1 in a2 or a2 in a1:
        return True
    for group in ACTION_SYNONYMS:
        if a1 in group and a2 in group:
            return True
    return False

def _subjects_conflict(sub1: Optional[str], sub2: Optional[str]) -> bool:
    """Returns True only if subjects clearly designate mutually exclusive entities."""
    if not sub1 or not sub2:
        return False
    s1, s2 = sub1.lower().strip(), sub2.lower().strip()
    if s1 == s2 or s1 in s2 or s2 in s1:
        return False
    generic = {"he", "she", "they", "it", "someone", "person", "man", "woman", "individual"}
    if s1 in generic or s2 in generic:
        return False
    suspect_group = {"suspect", "robber", "thief", "shooter", "assailant", "driver", "perpetrator"}
    if s1 in suspect_group and s2 in suspect_group:
        return False
    guard_group = {"guard", "security", "security guard", "officer", "police"}
    if s1 in guard_group and s2 in guard_group:
        return False
    if (s1 in suspect_group and s2 in guard_group) or (s1 in guard_group and s2 in suspect_group):
        return True
    return False

def _objects_are_compatible(obj1: Optional[str], obj2: Optional[str]) -> bool:
    """Checks whether two objects refer to compatible targets or overlap."""
    if not obj1 or not obj2:
        return True
    o1, o2 = obj1.lower().strip(), obj2.lower().strip()
    if o1 == o2 or o1 in o2 or o2 in o1:
        return True
    tokens1 = set(o1.split()) - {"a", "an", "the", "some", "his", "her", "their", "of", "in", "at", "on"}
    tokens2 = set(o2.split()) - {"a", "an", "the", "some", "his", "her", "their", "of", "in", "at", "on"}
    if tokens1 & tokens2:
        return True
    weapon_terms = {"gun", "weapon", "firearm", "pistol", "revolver", "rifle"}
    if (tokens1 & weapon_terms) and (tokens2 & weapon_terms):
        return True
    vehicle_terms = {"car", "sedan", "vehicle", "suv", "truck", "automobile"}
    if (tokens1 & vehicle_terms) and (tokens2 & vehicle_terms):
        return True
    return False

def check_existence_contradictions(occurrences: List[EventOccurrence], events: List[EventTuple]) -> List[DetectionResult]:
    """
    Checks for existence contradictions (Step 4).
    Compares explicit EventOccurrence denials against EventTuple assertions.
    """
    results = []
    
    for occ in occurrences:
        if occ.occurred is False:
            for ev in events:
                if occ.source_statement_id != ev.source_statement_id and not ev.negated:
                    if _actions_are_compatible(occ.event_type, ev.action):
                        results.append(DetectionResult(
                            claim_ids=[],
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
    refer to the same action/entity with compatible subject/object.
    """
    if claim1.negated != claim2.negated:
        if _subjects_conflict(claim1.subject, claim2.subject):
            return None
            
        act1 = (claim1.action or "").lower().strip()
        act2 = (claim2.action or "").lower().strip()
        
        actions_match = _actions_are_compatible(act1, act2)
        objects_match = _objects_are_compatible(claim1.object, claim2.object)
        
        perception_verbs = {"see", "saw", "notice", "noticed", "spot", "spotted", "observe", "observed", "have", "had"}
        perception_overlap = bool((act1 in perception_verbs or act2 in perception_verbs) and objects_match and (claim1.object and claim2.object))
        
        if (actions_match and objects_match) or perception_overlap:
            return DetectionResult(
                claim_ids=[],
                type="existence",
                verdict="contradiction",
                confidence=1.0,
                rationale="One witness explicitly negated this claim, while the other asserted it.",
                source_span=[(claim1.source_statement_id, claim1.source_span), (claim2.source_statement_id, claim2.source_span)]
            )
        
    return None
