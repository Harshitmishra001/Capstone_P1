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
            entities.append(Entity(
                source_statement_id=statement.id,
                source_span=(ent.start_char, ent.end_char),
                text=ent.text,
                label=domain_label,
                attributes={}
            ))
            
    return entities
