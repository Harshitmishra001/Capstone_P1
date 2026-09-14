"""
Extracts and normalizes temporal expressions (absolute or relative) from statements.
"""
from typing import List
from ml_core.schema.models import TemporalExpression, Statement

def extract_temporal_expressions(statement: Statement, anchor_time=None) -> List[TemporalExpression]:
    """Extracts and resolves time references."""
    pass
