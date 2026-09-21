"""
Extracts temporal expressions using spaCy and dateparser.
"""
import spacy
import dateparser
import logging
from typing import List
from ml_core.schema.models import TemporalExpression, Statement

logger = logging.getLogger(__name__)

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    logger.warning("spaCy 'en_core_web_sm' not found. Temporal extraction will be skipped.")
    nlp = None

def extract_temporal_references(statement: Statement) -> List[TemporalExpression]:
    if not nlp:
        return []
    
    doc = nlp(statement.text)
    temporals = []
    
    for ent in doc.ents:
        if ent.label_ in ["TIME", "DATE"]:
            # Parse the time string into a standard format
            parsed_date = dateparser.parse(ent.text)
            resolved_str = parsed_date.isoformat() if parsed_date else ent.text
            
            temporals.append(TemporalExpression(
                source_statement_id=statement.id,
                source_span=(ent.start_char, ent.end_char),
                text=ent.text,
                resolved_time=resolved_str
            ))
            
    return temporals
