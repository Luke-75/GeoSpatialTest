from src.ai import SearchRequest
import pytest
from pydantic import ValidationError


def test_valid_search_request():
    request = SearchRequest(
        location="Prague",
        limit=4,
        radius_km=10
    )

    assert request.location == "Prague"
    assert request.limit == 4
    #assert request.limit == 5
    assert request.radius_km == 10

# location tests

def test_empty_location_is_rejected():
    with pytest.raises(ValidationError):
        SearchRequest(
            location="",
            limit=4,
            radius_km=10
        )

def test_whitespace_location_is_rejected():
    with pytest.raises(ValidationError):
        SearchRequest(
            location="   ",
            limit=4,
            radius_km=10
        )

def test_location_whitespace_is_removed():
    request = SearchRequest(
        location="   Prague   ",
        limit=4,
        radius_km=10
    )

    assert request.location == "Prague"


# limit - boundary-value analysis tests
# (default=3, gt=0, le=10)

def test_limit_value_missing():
    request = SearchRequest(
        location="Prague",
        radius_km=10
    )

    assert request.limit == 3

def test_limit_below_min_rejected():
    with pytest.raises(ValidationError):
        SearchRequest(
            location="Prague",
            limit=0,
            radius_km=10
        )

def test_limit_at_min_ok():
    request = SearchRequest(
        location="Prague",
        limit=1,
        radius_km=10
    )
    
    assert request.limit == 1

def test_limit_in_range_ok():
    request = SearchRequest(
        location="Prague",
        limit=5,
        radius_km=10
    )
    
    assert request.limit == 5

def test_limit_at_max_ok():
    request = SearchRequest(
        location="Prague",
        limit=10,
        radius_km=10
    )
    
    assert request.limit == 10

def test_limit_above_max_rejected():
    with pytest.raises(ValidationError):
        SearchRequest(
            location="Prague",
            limit=11,
            radius_km=10
        )


# radius_km - boundary-value analysis tests
# (default=5, gt=0, le=50)

def test_radius_km_value_missing():
    request = SearchRequest(
        location="Prague",
        limit=5
    )

    assert request.radius_km == 5

def test_radius_km_below_min_rejected():
    with pytest.raises(ValidationError):
        SearchRequest(
            location="Prague",
            limit=5,
            radius_km=0
        )

def test_radius_km_just_above_min_ok():
    request = SearchRequest(
        location="Prague",
        limit=5,
        radius_km=0.1
    )
    
    assert request.radius_km == 0.1

def test_radius_km_in_range_ok():
    request = SearchRequest(
        location="Prague",
        limit=5,
        radius_km=20
    )
    
    assert request.radius_km == 20

def test_radius_km_at_max_ok():
    request = SearchRequest(
        location="Prague",
        limit=5,
        radius_km=50
    )
    
    assert request.radius_km == 50

def test_radius_km_above_max_rejected():
    with pytest.raises(ValidationError):
        SearchRequest(
            location="Prague",
            limit=5,
            radius_km=50.5
        )
