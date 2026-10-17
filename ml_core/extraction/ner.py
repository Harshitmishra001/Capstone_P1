"""
Extracts Named Entities (PERSON, VEHICLE, OBJECT, LOCATION) using spaCy.
Includes custom mapping for domain-specific attributes.
"""
import spacy
import logging
from typing import List
from ml_core.schema.models import Entity, Statement

logger = logging.getLogger(__name__)

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    logger.warning("spaCy 'en_core_web_sm' not found. NER will be skipped. Run 'python -m spacy download en_core_web_sm'")
    nlp = None

def extract_entities(statement: Statement) -> List[Entity]:
    """Runs NER on a statement text to extract structured Entities."""
    if not nlp:
        return []
    
    doc = nlp(statement.text)
    entities = []
    
    for ent in doc.ents:
        label = ent.label_
        domain_label = None
        
        # Map spaCy labels to our Domain Schema
        if label == "PERSON":
            domain_label = "PERSON"
        elif label in ["ORG", "PRODUCT"]:
            domain_label = "OBJECT"
        elif label in ["GPE", "LOC", "FAC"]:
            domain_label = "LOCATION"
        elif label == "NORP" or "car" in ent.text.lower() or "vehicle" in ent.text.lower():
            domain_label = "VEHICLE"
            
        if domain_label:
            attrs = {}
            text_lower = statement.text.lower()
            ent_lower = ent.text.lower()
            
            # Context window for attributes
            window_start = max(0, ent.start_char - 20)
            window_end = min(len(statement.text), ent.end_char + 20)
            window_text = text_lower[window_start:window_end]
            
            # Color attribute
            colors = ["red", "blue", "black", "white", "silver", "grey", "gray", "green", "yellow", "dark", "bright"]
            for c in colors:
                if c in window_text.split() or c in ent_lower.split():
                    attrs["color"] = c
                    break
                    
            # Vehicle type / make attribute
            if domain_label == "VEHICLE":
                for vtype in ["sedan", "suv", "motorcycle", "bike", "car", "truck", "van", "auto", "rickshaw"]:
                    if vtype in ent_lower or vtype in window_text.split():
                        attrs["make"] = vtype
                        break
                        
            # Person role attribute
            if domain_label == "PERSON":
                for role in ["robber", "suspect", "guard", "cashier", "clerk", "driver", "pedestrian", "man", "woman"]:
                    if role in ent_lower or role in window_text.split():
                        attrs["role"] = role
                        break

            entities.append(Entity(
                source_statement_id=statement.id,
                source_span=(ent.start_char, ent.end_char),
                text=ent.text,
                label=domain_label,
                attributes=attrs
            ))
            
    # Domain keyword scan for common vehicle mentions spaCy might miss
    vehicle_keywords = ["sedan", "suv", "motorcycle", "bike", "car", "truck", "auto-rickshaw", "rickshaw", "van"]
    existing_spans = [(e.source_span[0], e.source_span[1]) for e in entities]
    
    for word in vehicle_keywords:
        start = 0
        while True:
            idx = statement.text.lower().find(word, start)
            if idx == -1:
                break
            span = (idx, idx + len(word))
            if not any(max(span[0], s[0]) < min(span[1], s[1]) for s in existing_spans):
                window_start = max(0, idx - 15)
                window_text = statement.text.lower()[window_start:idx]
                attrs = {"make": word}
                for c in ["red", "blue", "black", "white", "silver", "grey", "gray", "green", "yellow", "dark"]:
                    if c in window_text.split():
                        attrs["color"] = c
                        break
                entities.append(Entity(
                    source_statement_id=statement.id,
                    source_span=span,
                    text=statement.text[idx:idx + len(word)],
                    label="VEHICLE",
                    attributes=attrs
                ))
                existing_spans.append(span)
            start = idx + len(word)
            
    return entities
