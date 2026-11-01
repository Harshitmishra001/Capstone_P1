"""
Extracts spatial and location references from raw text using spaCy.
Resolves coordinates using a deterministic offline landmark lookup table.
"""
import spacy
import logging
from typing import List, Optional, Tuple
from ml_core.schema.models import SpatialReference, Statement

logger = logging.getLogger(__name__)

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    logger.warning("spaCy 'en_core_web_sm' not found. Spatial extraction will be skipped.")
    nlp = None

# Offline reference coordinates for key locations to avoid external geocoding dependencies
OFFLINE_COORDINATES = {
    "mg road":          (12.9757, 77.6011),
    "commercial street":(12.9814, 77.6097),
    "indiranagar":      (12.9783, 77.6408),
    "chickpet":         (12.9641, 77.5759),
    "koramangala":      (12.9279, 77.6271),
    "tanishq":          (12.9752, 77.6072),
    "connaught place":  (28.6315, 77.2167),
    "chandni chowk":    (28.6562, 77.2310),
    "marine drive":     (18.9440, 72.8237),
    "mumbai":           (18.9220, 72.8347),
    "mumbai port":      (18.9500, 72.8500),
    "delhi":            (28.6139, 77.2090),
    "new delhi":        (28.6139, 77.2090),
    "bengaluru":        (12.9716, 77.5946),
    "bangalore":        (12.9716, 77.5946),
    "main st":          (40.7128, -74.0060),
    "main street":      (40.7128, -74.0060),
}

def resolve_offline_coordinates(name: str) -> Optional[Tuple[float, float]]:
    """Resolves coordinates offline without external API dependencies."""
    clean = name.strip().lower()
    for key, coords in OFFLINE_COORDINATES.items():
        if key in clean or clean in key:
            return coords
    return None

def extract_spatial_references(statement: Statement) -> List[SpatialReference]:
    """Runs NER to extract locations and resolves coordinates offline where known."""
    if not nlp:
        return []
        
    doc = nlp(statement.text)
    spatials = []
    
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC", "FAC"]:
            coords = resolve_offline_coordinates(ent.text)
            spatials.append(SpatialReference(
                source_statement_id=statement.id,
                source_span=(ent.start_char, ent.end_char),
                text=ent.text,
                resolved_coordinates=coords,
                resolved=coords is not None
            ))
            
    return spatials
