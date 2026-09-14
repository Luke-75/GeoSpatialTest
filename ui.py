#ui.py

import streamlit as st
import pandas as pd
import geopandas as gpd
import re
from geo import format_distance
from pyproj import Transformer
import folium
from streamlit_folium import st_folium

fmap: folium.map
dataframe: pd.DataFrame


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

#def draw_map(coords_wgs84: list[dict]):
def draw_map(data_frame: pd.DataFrame):
    st.subheader("Map")

    """
    st.map(
            coords_wgs84,
            latitude="lat",
            longitude="lon",
            color="color",
            size=120,
        )
    """

    with st.container(border=True):

        global fmap
        global dataframe
        # Create map centered on searched location (first point in the dataframe)
        fmap = folium.Map(
            location=[data_frame.loc[0]['lat'], data_frame.loc[0]['lon']],
            tiles="OpenStreetMap", 
            zoom_start=14
        )

        #add markers fo reach dataframe row
        for i in range(0,len(data_frame)):
            folium.Marker(
                location=[data_frame.iloc[i]['lat'], data_frame.iloc[i]['lon']],
                popup=data_frame.iloc[i]['name'],
                tooltip=data_frame.iloc[i]['name'],
                icon=folium.Icon(icon="star",color=data_frame.iloc[i]['icon_color']),
            ).add_to(fmap)

        # Display the stored map
        map_data = st_folium(
            fmap,
            width=700, 
            height=500,
            returned_objects=[]
        )



def display_search_results(srch_results: list[dict], srch_lat, srch_lon):
    #raw geo data for debugging
    #st.write(srch_results)

    st.write(f"Location in a map: https://www.google.com/maps?ll={srch_lat},{srch_lon};")

    global dataframe
    dataframe = pd.DataFrame({
        'lat':[srch_lat],
        'lon':[srch_lon],
        'name':['Search Location'],
        'icon_color':['green']
    }, dtype=str)
    
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

            #add a new row to the dataframe using loc[]
            #attributes: [latitude, longitude, name, icon_color]
            dataframe.loc[len(dataframe)] = [loc_y, loc_x, name, 'blue']

            st.write(f"https://www.google.com/maps?ll={loc_y},{loc_x};")
           
    # show search center and search results on map
    #draw_map(nearest_wgs84)
    draw_map(dataframe)

