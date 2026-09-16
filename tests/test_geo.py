#from src.geo import format_distance
from src.geo import format_distance, find_nearest_stations, query_petrol_stations, geocode
from unittest.mock import patch


def test_format_distance_far_below_one_km():
    assert format_distance(100) == "100 m"


def test_format_distance_just_below_one_km():
    assert format_distance(999.9) == "1 km"


def test_format_distance_exactly_one_km():
    assert format_distance(1000) == "1 km"


def test_format_distance_just_above_one_km():
    assert format_distance(1000.5) == "1 km"


def test_format_distance_decimal_km():
    assert format_distance(1200) == "1.2 km"


def test_format_distance_decimal_km():
    assert format_distance(1260) == "1.3 km"


def test_format_distance_two_km():
    assert format_distance(2000) == "2 km"


# testing find_nearest_stations()

import pandas as pd
import geopandas
#from src.geo import format_distance, find_nearest_stations


def test_find_nearest_stations_returns_nearest_within_limit():
    """
    A: lat 50.000, lon 14.000
    B: lat 50.001, lon 14.000
    C: lat 50.002, lon 14.000
    D: lat 50.003, lon 14.000
    E: lat 50.004, lon 14.000
    F: lat 50.005, lon 14.000
    """

    df = pd.DataFrame(
        {
            "Name" : ["A","B","C","D","E","F"],
            "Latitude": [50.000, 50.001, 50.002, 50.003, 50.004, 50.005],
            "Longitude": [14.000, 14.000, 14.000, 14.000, 14.000, 14.000],
        }
    )

    gdf = geopandas.GeoDataFrame(
        df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude), crs="EPSG:4326"
    )

    result = find_nearest_stations(
        lat=50.0,
        lon=14.0,
        stations=gdf,
        limit=3
    )

    assert len(result) == 3
    assert result["Name"].tolist() == ["A", "B", "C"]
    assert result.iloc[0]["distance_m"] == 0


def test_find_nearest_stations_with_empty_gdf():
    empty_gdf = geopandas.GeoDataFrame(
        {"Name": []},
        geometry=[],
        crs="EPSG:4326"
    )
    
    result = find_nearest_stations(
        lat=50.0,
        lon=14.0,
        stations=empty_gdf,
        limit=3
    )

    assert result is None


#from src.geo import query_petrol_stations

def test_query_petrol_stations_returns_found_stations():
    test_gdf = geopandas.GeoDataFrame(
        {
            "Name": ["Station A", "Station B"]
        },
        geometry=geopandas.points_from_xy(
            [14.0, 14.01],
            [50.0, 50.01]
        ),
        crs="EPSG:4326"
    )

    with patch("osmnx.features_from_point") as mock_features:
        mock_features.return_value = test_gdf

        result = query_petrol_stations(
            lat=50.0,
            lon=14.0,
            radius_m=5000
        )

        assert result is test_gdf
        mock_features.assert_called_once_with(
            (50.0, 14.0),
            tags={"amenity": "fuel"},
            dist=5000
        )


def test_query_petrol_stations_returns_none_when_no_stations_found():
    empty_gdf = geopandas.GeoDataFrame(
        geometry=[],
        crs="EPSG:4326"
    )

    with patch("osmnx.features_from_point") as mock_features:
        mock_features.return_value = empty_gdf

        result = query_petrol_stations(
            lat=50.0,
            lon=14.0,
            radius_m=5000
        )

        assert result is None


def test_query_petrol_stations_invalid_coordinates():
    with patch("osmnx.features_from_point") as mock_features:

        result = query_petrol_stations(
            lat=100,
            lon=14,
            radius_m=5000
        )

        assert result is None
        mock_features.assert_not_called()


def test_query_petrol_stations_handles_osm_failure():
    with patch("osmnx.features_from_point") as mock_features:
        mock_features.side_effect = RuntimeError(
            "OSM service unavailable"
        )

        result = query_petrol_stations(
            lat=50.0,
            lon=14.0,
            radius_m=5000
        )

        assert result is None
        mock_features.assert_called_once_with(
            (50.0, 14.0),
            tags={"amenity": "fuel"},
            dist=5000
        )


#from src.geo import geocode
"""
def test_geocode_returns_coordinates():
    with patch.dict(
        "os.environ",
        {"NOMINATIM_USER_AGENT_NAME": "test-agent"}
    ):
        with patch("geopy.geocoders.Nominatim") as mock_nominatim:
            mock_geolocator = mock_nominatim.return_value

            mock_location = mock_geolocator.geocode.return_value
            mock_location.latitude = 50.0755
            mock_location.longitude = 14.4378

            result = geocode("Prague")

            assert result == {50.0755, 14.4378}
            mock_geolocator.assert_called_once_with(
                "Prague"
            )
"""
