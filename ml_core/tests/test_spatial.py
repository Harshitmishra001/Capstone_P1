import pytest
from ml_core.schema.models import Statement
from ml_core.extraction.spatial import extract_spatial_references, resolve_offline_coordinates

def test_resolve_offline_coordinates_known():
    coords = resolve_offline_coordinates("MG Road")
    assert coords is not None
    assert round(coords[0], 2) == 12.98
    assert round(coords[1], 2) == 77.60

def test_resolve_offline_coordinates_unknown():
    coords = resolve_offline_coordinates("Random Unmapped Village 123")
    assert coords is None

def test_extract_spatial_references():
    stmt = Statement(
        id="s1",
        witness_id="w1",
        text="The incident occurred near Marine Drive in Mumbai.",
        incident_id="inc1"
    )
    spatials = extract_spatial_references(stmt)
    assert len(spatials) >= 1
    # Check that at least one location resolved to coordinates
    has_resolved = any(s.resolved for s in spatials)
    assert has_resolved is True
