#utils.py

import streamlit as st
import pandas as pd
import geopandas as gpd
import re
from geo import format_distance
from pyproj import Transformer

def remove_extra_spaces(text: str) -> str:
    """
    Removes multiple consecutive spaces from a string, replacing them with a single space.
    Leading and trailing spaces are also trimmed.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    # Replace 2 or more spaces with a single space
    cleaned_text = re.sub(r' {2,}', ' ', text)

    # Strip leading/trailing spaces
    return cleaned_text.strip()

def draw_map(coords_wgs84: list[dict]):
    st.subheader("Map")

    #st.map(
    #    coords_wgs84[["lat", "lon"]]
    #)

    st.map(
            coords_wgs84,
            latitude="lat",
            longitude="lon",
            color="color",
            size=120,
        )

def display_search_results(srch_results: list[dict], srch_lat, srch_lon):
    #raw geo data for debugging
    #st.write(srch_results)

    colors = [
        "#e6194b",
        "#3cb44b",
        "#4363d8",
        "#f58231",
        "#911eb4",
        "#42d4f4",
        "#f032e6",
        "#bfef45",
        "#fabed4",
        "#469990",
    ]

    types = [
        "Station 1",
        "Station 2",
        "Station 3",
        "Station 4",
        "Station 5",
        "Station 6",
        "Station 7",
        "Station 8",
        "Station 9",
        "Station 10",
    ]

    st.write(f"Location in a map: https://www.google.com/maps?ll={srch_lat},{srch_lon};")
    
    for i, station in srch_results.iterrows():

        name = station.get("name") or "Unnamed petrol station"
        brand_name = station.get("brand") or "<Unknown brand>"
    
        address_city = str(station.get("addr:city") or "")
        if address_city == "nan":
            address_city = ""
        address_place = str(station.get("addr:place") or "")
        if address_place == "nan":
            address_place = ""
        address_postcode = str(station.get("addr:postcode") or "")
        if address_postcode == "nan":
            address_postcode = ""
        address_street = str(station.get("addr:street") or "")
        if address_street == "nan":
            address_street = ""
        address_housenumber = str(station.get("addr:housenumber") or "")
        if address_housenumber == "nan":
            address_housenumber = ""

        # retrieving lat and lon to be used to generate Google Maps link
        # https://www.bing.com/search?q=python+point+object+tocrs&cvid=95188882a0834a35b8d7a14b52bd073e&gs_lcrp=EgRlZGdlKgYIABBFGDkyBggAEEUYOdIBCTE3MTcxajBqNKgCCLACAQ&FORM=ANAB01&PC=U531
        xlat = station.get("geometry")
        gseries = gpd.GeoSeries([xlat])
        rep_point = gseries.representative_point()[0]
        transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
        loc_x, loc_y = transformer.transform(rep_point.x, rep_point.y)
                                                 
        address = remove_extra_spaces(address_postcode + " " + address_city + " " + address_place + " " + address_street + " " + address_housenumber)
        opening_hours = station.get("opening_hours") or "NA"
        distance = format_distance(station["distance_m"])
    
        with st.container(border=True):
            st.markdown(f"### ⛽ {name}")
            st.write(f"**Brand:** {brand_name}")
            st.write(f"**Address:** {address}")
            st.write(f"**Opening hours:** {opening_hours}")
            st.write(f"**Distance:** {distance}")
    
            if station.get("address"):
                st.write(f"**Address:** {station['address']}")
    
            # coordinates to show on map
            nearest_wgs84 = srch_results.to_crs(epsg=4326)
    
            nearest_wgs84["point"] = nearest_wgs84.geometry.representative_point()
            nearest_wgs84["lat"] = nearest_wgs84["point"].y
            nearest_wgs84["lon"] = nearest_wgs84["point"].x

            st.write(f"https://www.google.com/maps?ll={loc_y},{loc_x};")
           
    
    # visualize the search center point
    search_center = pd.DataFrame({
        "lat": [srch_lat],
        "lon": [srch_lon],
        "type": ["Search location"],
        "color": ["#11EAE0"],
    })

    nearest_wgs84["color"] = colors[:len(nearest_wgs84)]
    nearest_wgs84["type"] = types[:len(nearest_wgs84)]
    
    
    # concatenate results coordinates with the search center
    map_data = pd.concat(
        [
            search_center,
            nearest_wgs84[["lat", "lon", "type", "color"]],
        ],
        ignore_index=True,
    )
    
    # show search center and search results on map
    #draw_map(nearest_wgs84)
    draw_map(map_data)

