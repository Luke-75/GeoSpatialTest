# geo.py

def geocode(address: str) -> tuple[float, float]:
    from geopy.geocoders import Nominatim

    user_agent_name = "LK_Demo_Test"
    geolocator = Nominatim(user_agent=user_agent_name)
    location = geolocator.geocode(
        query = address
    )
    if location:
        return{
            location.latitude,
            location.longitude 
        }
    else:
        raise ValueError(f"Could not find location for address: {address}")
    

def query_petrol_stations(
    lat: float,
    lon: float,
    radius_m: int = 5000,
) -> list[dict]:

    import osmnx as ox
    import geopandas as gpd
    from shapely.geometry import Point

    try:
        # Validate coordinates
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise ValueError("Invalid latitude or longitude values.")
    
        # Create a point geometry for the search center
        center_point = Point(lon, lat)
    
        # Build Overpass query for 'amenity=fuel' within radius
        tags = {"amenity": "fuel"}
        """
        In recent versions of OSMnx (≥2.0), the function geometries_from_point was removed/renamed as part of the API changes.
        """
        #gdf = ox.geometries_from_point((lat, lon), tags=tags, dist=radius_m)
        gdf = ox.features_from_point((lat, lon), tags=tags, dist=radius_m)
    
        if gdf.empty:
            print("No petrol stations found within the search radius.")
            return None
        else:
            return gdf

    except Exception as e:
        print(f"Error: {e}")
        return None


def find_nearest_stations(
    lat: float,
    lon: float,
    stations: list[dict],
    limit: int = 3,
) -> list[dict]:

    import geopandas as gpd
    from shapely.geometry import Point

    # Create a point geometry for the search center
    center_point = Point(lon, lat)

    #raw geo data for debugging
    #print(stations)

    """
    # converting list to points
    tmp_gdf = gpd.GeoDataFrame(
        stations,
        geometry=[Point(row["lon"], row["lat"]) for row in stations],
        crs="EPSG:4326"
    )
    """

    # Ensure geometry is in correct CRS for distance calculation
    #gdf = tmp_gdf.to_crs(epsg=3857)
    gdf = stations.to_crs(epsg=3857)
    center_geom = gpd.GeoSeries([center_point], crs="EPSG:4326").to_crs(epsg=3857)
    
    # Calculate distances and find the nearest
    gdf["distance_m"] = gdf.geometry.distance(center_geom.iloc[0])
    nearest = gdf.sort_values("distance_m").iloc[0:limit]

    if nearest.empty:
        return None
    else:
        return nearest


def format_distance(distance_m):
    if distance_m < 1000:
        return f"{distance_m:.0f} m"
    return f"{distance_m / 1000:.1f} km"

