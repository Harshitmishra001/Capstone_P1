"""
Extracts spatial and location references from raw text using spaCy.
"""
import spacy
import logging
from typing import List
from ml_core.schema.models import SpatialReference, Statement

logger = logging.getLogger(__name__)

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    logger.warning("spaCy 'en_core_web_sm' not found. Spatial extraction will be skipped.")
    nlp = None

def extract_spatial_references(statement: Statement) -> List[SpatialReference]:
    if not nlp:
        return []
        
    doc = nlp(statement.text)
    spatials = []
    
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC", "FAC"]:
            spatials.append(SpatialReference(
                source_statement_id=statement.id,
                source_span=(ent.start_char, ent.end_char),
                text=ent.text,
                resolved_coordinates=None, # Explicitly keeping as None to avoid external Geocoding APIs for now
                resolved=False
            ))
            
    return spatials
