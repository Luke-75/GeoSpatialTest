import streamlit as st
import pandas as pd

from src.geo import geocode, query_petrol_stations, find_nearest_stations
from src.ai import SearchRequest, parse_search_query
from src.ui import remove_extra_spaces, draw_map, display_search_results
from pydantic import ValidationError




st.title("Nearest Petrol Stations")


ai_query = st.text_input("Enter address or Type a query for AI", key="ai_query_textbox")

if st.button("Find stations") and ai_query:

    search_query = parse_search_query(ai_query)

    # for debug purposes
    #st.write(search_query)

    if search_query is not None:

        lat, lon = geocode(search_query.location)

        stations = query_petrol_stations(lat, lon)
    
        if stations.empty:
            print("No results returned.")
        else:
            nearest = find_nearest_stations(
                lat,
                lon,
                stations,
                limit=search_query.limit,
            )
                
            #raw geo data for debugging
            #st.write(search_query)
                
            display_search_results(nearest, lat, lon, search_query.radius_km)

