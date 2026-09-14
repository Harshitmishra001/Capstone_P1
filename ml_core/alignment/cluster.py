"""
Aligns claims across different witnesses that refer to the same underlying entity or event.
Uses sentence-transformers embedding similarity + entity overlap + time window.
"""
from typing import List
from ml_core.schema.models import Claim

def align_claims(claims: List[Claim]) -> List[List[Claim]]:
    """
    Clusters extracted claims into aligned groups for contradiction detection.
    Returns a list of claim clusters (where each cluster contains claims referring to the same event/entity).
    """
    pass
