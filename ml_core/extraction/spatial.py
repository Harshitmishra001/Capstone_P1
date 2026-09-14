"""
Extracts spatial references and resolves them to coordinates via external geocoding where possible.
"""
from typing import List
from ml_core.schema.models import SpatialReference, Statement

def extract_spatial_references(statement: Statement) -> List[SpatialReference]:
    """Extracts locations and geocodes them."""
    pass
