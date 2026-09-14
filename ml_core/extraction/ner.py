"""
Extracts Named Entities (PERSON, VEHICLE, OBJECT, LOCATION) using spaCy.
Includes custom EntityRuler for domain-specific attributes (e.g. vehicle color/make).
"""
from typing import List
from ml_core.schema.models import Entity, Statement

def extract_entities(statement: Statement) -> List[Entity]:
    """Runs NER on a statement text to extract structured Entities."""
    pass
